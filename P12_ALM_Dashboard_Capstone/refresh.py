# refresh.py — Rebuild ALM Dashboard from data.py
# Run this directly: python refresh.py
# Or click the Refresh button inside ALM_Dashboard.xlsm
#
# ── CONFIG — update these paths for your environment ─────────────────────────
import os
SAVE_PATH   = r"C:\Users\hossa\Desktop\ALM_Dashboard.xlsx"   # output file

import xlwings as xw
import data
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import tempfile

print("Refreshing ALM Dashboard...")

try:
    # ── Open workbook ──────────────────────────────────────────────────────────
    app = xw.App(visible=True, add_book=False)
    app.display_alerts = False
    wb  = app.books.add()

    # Colour palette
    NAVY      = (0,  107,  63)     # G-SIB brand green — column headers
    MID_BLUE  = (0,  150,  94)     # G-SIB brand green — section dividers
    LT_GREY   = (242, 242, 242)
    WHITE     = (255, 255, 255)
    C_GREEN   = (0,  176,  80)
    C_AMBER   = (255, 192,   0)
    C_RED     = (192,   0,   0)
    C_GRN_TXT = (0,   97,   0)
    C_RED_TXT = (255, 255, 255)

    def rag(value, green_fn, amber_fn=None):
        if green_fn(value):                return "GREEN"
        elif amber_fn and amber_fn(value): return "AMBER"
        else:                              return "RED"

    def rag_color(status):
        return {"GREEN": (C_GREEN, C_GRN_TXT),
                "AMBER": (C_AMBER, (0, 0, 0)),
                "RED":   (C_RED,   C_RED_TXT)}[status]

    def fmt_header(rng):
        rng.color = NAVY; rng.font.color = WHITE
        rng.font.bold = True; rng.font.size = 10

    def fmt_section(rng):
        rng.color = MID_BLUE; rng.font.color = WHITE
        rng.font.bold = True; rng.font.size = 10

    def fmt_title(cell, text):
        cell.value = text; cell.font.bold = True
        cell.font.size = 14; cell.font.color = NAVY

    def fmt_subtitle(cell, text):
        cell.value = text; cell.font.size = 10
        cell.font.color = (89, 89, 89)

    def apply_rag_cell(cell, status):
        bg, txt = rag_color(status)
        cell.color = bg; cell.font.color = txt
        cell.font.bold = True; cell.value = status

    def shade_row(rng, i):
        rng.color = LT_GREY if i % 2 == 0 else WHITE

    def set_cols(sheet, widths):
        for col, w in widths.items():
            sheet.range(f"{col}:{col}").column_width = w

    print("Helper functions loaded ✓")
    wb.sheets[0].name = "ALCO Scorecard"

    for name in ["Interest Rate Risk", "Liquidity", "Capital",
                 "Market Risk", "FTP & Behavioural"]:
        wb.sheets.add(name, after=wb.sheets[-1])

    print(f"Sheets created ({len(wb.sheets)} total):")
    for s in wb.sheets:
        print(f"  • {s.name}")
    ws = wb.sheets["ALCO Scorecard"]
    set_cols(ws, {"A": 20, "B": 38, "C": 22, "D": 18, "E": 16, "F": 12})

    fmt_title(ws["B1"], "ALCO Management Information Pack")
    fmt_subtitle(ws["B2"], "Major European G-SIB  |  31 Dec 2025A / 2026F  |  Base + Severe Stress")
    fmt_subtitle(ws["B3"], "Prepared by: ALM / Treasury  |  Classification: Confidential")
    ws["A1"].row_height = 28

    for i, h in enumerate(["RISK BLOCK", "METRIC", "REGULATORY LIMIT",
                            "CURRENT VALUE", "HEADROOM", "STATUS"]):
        ws[f"{'ABCDEF'[i]}5"].value = h
    fmt_header(ws["A5:F5"])
    ws["A5"].row_height = 22

    scorecard = [
        (True,  "NII RISK",     None, None, None, None, None),
        (False, "NII Risk",     "Stressed NII / Base NII",          "> 75% of Base",    "67.6%",        "-7.4pp",    rag(67.6,   lambda v: v>=85,   lambda v: v>=75)),
        (False, "NII Risk",     "Worst NII vs Base",                "> -6,000m",        "-5,893m",      "+107m",     rag(-5893,  lambda v: v>=-6000)),
        (True,  "IRRBB / EVE", None, None, None, None, None),
        (False, "IRRBB / EVE", "Net EVE / Tier 1 (hedged, worst)", "< 15% T1",         "13.24%",       "1.76pp",    rag(13.24,  lambda v: v<12,    lambda v: v<15)),
        (False, "IRRBB / EVE", "EVE / Tier 1 (ICAAP severe)",      "< 15% T1",         "19.87%",       "-4.87pp",   rag(19.87,  lambda v: v<12,    lambda v: v<15)),
        (True,  "LIQUIDITY",   None, None, None, None, None),
        (False, "Liquidity",   "LCR - Base",                       "> 100%",           "153.4%",       "+53.4pp",   rag(153.4,  lambda v: v>=110,  lambda v: v>=100)),
        (False, "Liquidity",   "NSFR - Base",                      "> 100%",           "102.2%",       "+2.2pp",    rag(102.2,  lambda v: v>=110,  lambda v: v>=100)),
        (False, "Liquidity",   "NSFR - Stress",                    "> 100%",           "99.8%",        "-0.2pp",    rag(99.8,   lambda v: v>=110,  lambda v: v>=100)),
        (False, "Liquidity",   "Survival Horizon - Stress",         "> 3 months",       "2 months",     "-1 month",  rag(2,      lambda v: v>=3,    lambda v: v>=1)),
        (True,  "CAPITAL",     None, None, None, None, None),
        (False, "Capital",     "CET1 Ratio - Base 2026F",          "> 9.50% (MDA)",    "15.88%",       "+6.38pp",   rag(15.88,  lambda v: v>=12,   lambda v: v>=10)),
        (False, "Capital",     "MDA Buffer",                       "> 1.00pp",         "+5.66pp",      "+4.66pp",   rag(5.66,   lambda v: v>=2,    lambda v: v>=1)),
        (False, "Capital",     "Leverage Ratio",                   "> 3.50% (G-SIB)",  "5.29%",        "+1.79pp",   rag(5.29,   lambda v: v>=4,    lambda v: v>=3.5)),
        (True,  "MARKET RISK", None, None, None, None, None),
        (False, "Market Risk", "Portfolio DV01",                   "< 120m per bp",    "100.88m/bp",   "+19.1m",    rag(100.88, lambda v: v<=110,  lambda v: v<=120)),
        (False, "Market Risk", "+200bps P&L / Portfolio MV",       "> -15%",           "-11.7%",       "+3.3pp",    rag(-11.7,  lambda v: v>=-12,  lambda v: v>=-15)),
    ]

    START_ROW  = 6
    data_count = 0
    for i, row in enumerate(scorecard):
        r = START_ROW + i
        is_hdr, block, metric, limit, current, headroom, status = row
        if is_hdr:
            ws[f"A{r}"].value = block
            fmt_section(ws[f"A{r}:F{r}"])
            ws[f"A{r}"].row_height = 20
        else:
            shade_row(ws[f"A{r}:E{r}"], data_count)
            ws[f"A{r}"].value = block
            ws[f"B{r}"].value = metric
            ws[f"C{r}"].value = limit
            ws[f"D{r}"].value = current
            ws[f"E{r}"].value = headroom
            apply_rag_cell(ws[f"F{r}"], status)
            ws[f"A{r}:F{r}"].font.size = 10
            ws[f"A{r}"].row_height = 18
            data_count += 1

    print("Sheet 1 - ALCO Scorecard ✓")

    # ── Sheet 2: Interest Rate Risk ───────────────────────────────────────────────
    ws2 = wb.sheets["Interest Rate Risk"]
    set_cols(ws2, {"A": 22, "B": 16, "C": 15, "D": 16, "E": 16, "F": 16, "G": 12})

    fmt_title(ws2["B1"], "Interest Rate Risk — NII & EVE Sensitivity")
    fmt_subtitle(ws2["B2"], "Major European G-SIB  |  2026F Forecast  |  Sources: P1 (NII) + P9 (EVE)")
    ws2["A1"].row_height = 28

    # PART A — NII
    ws2["A4"].value = "PART A — NET INTEREST INCOME (NII) SENSITIVITY"
    fmt_section(ws2["A4:G4"])
    ws2["A4"].row_height = 20

    for i, h in enumerate(["SCENARIO", "RATE SHOCK", "DEPOSIT BETA",
                            "NII (Eur m)", "DELTA vs BASE (Eur m)", "DELTA vs BASE (%)", "STATUS"]):
        ws2[f"{'ABCDEFG'[i]}5"].value = h
    fmt_header(ws2["A5:G5"])
    ws2["A5"].row_height = 22

    base_nii = data.P1["base_nii"]
    nii_rows = [
        ("Base",       "0 bp",      "0.40",  22085,    0,     0.0),
        ("Rate Hike",  "+200 bps",  "0.50",  23676,  +1591,  +7.2),
        ("Rate Cut",   "-200 bps",  "0.30",  16192,  -5893, -26.7),
        ("Stress",     "+300 bps",  "0.60",  21245,  -840,   -3.8),
    ]

    for i, (scenario, shock, beta, nii, delta, delta_pct) in enumerate(nii_rows):
        r = 6 + i
        shade_row(ws2[f"A{r}:F{r}"], i)
        ws2[f"A{r}"].value = scenario
        ws2[f"B{r}"].value = shock
        ws2[f"C{r}"].value = beta
        ws2[f"D{r}"].value = nii
        ws2[f"E{r}"].value = delta
        ws2[f"F{r}"].value = f"{delta_pct:+.1f}%"
        status = rag(nii, lambda v: v >= base_nii * 0.85, lambda v: v >= base_nii * 0.75)
        apply_rag_cell(ws2[f"G{r}"], status)
        ws2[f"A{r}:G{r}"].font.size = 10
        ws2[f"A{r}"].row_height = 18

    # PART B — EVE
    ws2["A11"].value = "PART B — ECONOMIC VALUE OF EQUITY (DELTA EVE)  |  Net of 55% IRS Hedge  |  Tier 1 = Eur 132,173m"
    fmt_section(ws2["A11:G11"])
    ws2["A11"].row_height = 20

    for i, h in enumerate(["SCENARIO", "SHOCK", "GROSS EVE (Eur m)",
                            "HEDGE OFFSET (Eur m)", "NET EVE (Eur m)", "NET EVE / T1", "STATUS"]):
        ws2[f"{'ABCDEFG'[i]}12"].value = h
    fmt_header(ws2["A12:G12"])
    ws2["A12"].row_height = 22

    eve_rows = [
        ("Parallel Up",     "+200 bps",  38902,  21396,  17506,  13.24),
        ("Parallel Down",   "-200 bps",  33067,  18187,  14880,  11.26),
        ("Steepener",       "+90/-90",   17821,   9801,   8019,   6.07),
        ("Flattener",       "-90/+90",   17821,   9801,   8019,   6.07),
        ("Short Rate Up",   "+250 bps",    437,    240,    197,   0.15),
        ("Short Rate Down", "-250 bps",    372,    204,    167,   0.13),
    ]

    for i, (scenario, shock, gross, hedge, net, t1_pct) in enumerate(eve_rows):
        r = 13 + i
        shade_row(ws2[f"A{r}:F{r}"], i)
        ws2[f"A{r}"].value = scenario
        ws2[f"B{r}"].value = shock
        ws2[f"C{r}"].value = gross
        ws2[f"D{r}"].value = hedge
        ws2[f"E{r}"].value = net
        ws2[f"F{r}"].value = f"{t1_pct:.2f}%"
        status = rag(t1_pct, lambda v: v < 12, lambda v: v < 15)
        apply_rag_cell(ws2[f"G{r}"], status)
        ws2[f"A{r}:G{r}"].font.size = 10
        ws2[f"A{r}"].row_height = 18

    ws2["A20"].value = "Note: Unhedged Gross EVE (Par Up) = Eur 38,902m = 29.4% T1. IRS overlay reduces to 13.24% — within 15% outlier threshold."
    ws2["A20"].font.size = 9
    ws2["A20"].font.color = (89, 89, 89)
    ws2["A20"].font.italic = True

    print("Sheet 2 — Interest Rate Risk ✓")

    # ── Sheet 3: Liquidity ────────────────────────────────────────────────────────
    ws3 = wb.sheets["Liquidity"]
    set_cols(ws3, {"A": 22, "B": 16, "C": 14, "D": 16, "E": 14, "F": 18, "G": 12})

    fmt_title(ws3["B1"], "Liquidity Risk — LCR / NSFR / Maturity Ladder")
    fmt_subtitle(ws3["B2"], "Major European G-SIB  |  2026F Forecast  |  Sources: P3 (LCR/NSFR) + P10 (Maturity Ladder)")
    ws3["A1"].row_height = 28

    # PART A — LCR / NSFR by Scenario
    ws3["A4"].value = "PART A — LCR / NSFR BY SCENARIO"
    fmt_section(ws3["A4:G4"])
    ws3["A4"].row_height = 20

    for i, h in enumerate(["SCENARIO", "LCR (%)", "LCR STATUS",
                            "NSFR (%)", "NSFR STATUS", "NMD STABLE %", "BINDING"]):
        ws3[f"{'ABCDEFG'[i]}5"].value = h
    fmt_header(ws3["A5:G5"])
    ws3["A5"].row_height = 22

    lcr_rows = [
        ("Base",       153.4, 102.2, "70%"),
        ("Rate Hike",  153.9, 101.9, "65%"),
        ("Rate Cut",   152.9, 102.2, "72%"),
        ("Stress",     155.1,  99.8, "50%"),
    ]

    for i, (scenario, lcr, nsfr, nmd) in enumerate(lcr_rows):
        r = 6 + i
        shade_row(ws3[f"A{r}:F{r}"], i)
        ws3[f"A{r}"].value = scenario
        ws3[f"B{r}"].value = f"{lcr:.1f}%"
        apply_rag_cell(ws3[f"C{r}"], rag(lcr,  lambda v: v>=110, lambda v: v>=100))
        ws3[f"D{r}"].value = f"{nsfr:.1f}%"
        apply_rag_cell(ws3[f"E{r}"], rag(nsfr, lambda v: v>=110, lambda v: v>=100))
        ws3[f"F{r}"].value = nmd
        # binding constraint — NSFR is tighter than LCR in all scenarios
        ws3[f"G{r}"].value = "NSFR"
        ws3[f"G{r}"].font.size = 10
        ws3[f"A{r}:G{r}"].font.size = 10
        ws3[f"A{r}"].row_height = 18

    # PART B — HQLA Composition
    ws3["A11"].value = "PART B — HQLA COMPOSITION  |  Total HQLA = Eur 364,437m"
    fmt_section(ws3["A11:G11"])
    ws3["A11"].row_height = 20

    for i, h in enumerate(["ASSET CLASS", "LEVEL", "BALANCE (Eur m)", "SHARE (%)", "HAIRCUT", "POST-HAIRCUT (Eur m)"]):
        ws3[f"{'ABCDEF'[i]}12"].value = h
    fmt_header(ws3["A12:F12"])
    ws3["A12"].row_height = 22

    hqla_rows = [
        ("Cash & CB Reserves",  "Level 1",  211330, 58.0, "0%",   211330),
        ("Government Bonds",    "Level 1",  110237, 30.3, "0%",   110237),
        ("Corporate Bonds IG",  "Level 2A",  42870, 11.8, "15%",   36440),
        ("TOTAL HQLA",          "",         364437, 100.0, "",     357977),
    ]

    for i, (asset, level, bal, share, haircut, post) in enumerate(hqla_rows):
        r = 13 + i
        shade_row(ws3[f"A{r}:F{r}"], i)
        ws3[f"A{r}"].value = asset
        ws3[f"B{r}"].value = level
        ws3[f"C{r}"].value = bal
        ws3[f"D{r}"].value = f"{share:.1f}%"
        ws3[f"E{r}"].value = haircut
        ws3[f"F{r}"].value = post
        ws3[f"A{r}:F{r}"].font.size = 10
        ws3[f"A{r}"].row_height = 18
        if asset == "TOTAL HQLA":
            ws3[f"A{r}:F{r}"].font.bold = True

    # PART C — Survival Horizon
    ws3["A18"].value = "PART C — MATURITY LADDER  |  Survival Horizon (Repo 30% Frozen + 10% Deposit Flight)"
    fmt_section(ws3["A18:G18"])
    ws3["A18"].row_height = 20

    for i, h in enumerate(["SCENARIO", "SURVIVAL HORIZON", "vs ILAAP THRESHOLD (3M)", "STATUS"]):
        ws3[f"{'ABCD'[i]}19"].value = h
    fmt_header(ws3["A19:D19"])
    ws3["A19"].row_height = 22

    horizon_rows = [
        ("Base",   "9 months", "+6 months",  rag(9,  lambda v: v>=6, lambda v: v>=3)),
        ("Stress", "2 months", "-1 month",   rag(2,  lambda v: v>=6, lambda v: v>=3)),
    ]

    for i, (scenario, horizon, vs_threshold, status) in enumerate(horizon_rows):
        r = 20 + i
        shade_row(ws3[f"A{r}:C{r}"], i)
        ws3[f"A{r}"].value = scenario
        ws3[f"B{r}"].value = horizon
        ws3[f"C{r}"].value = vs_threshold
        apply_rag_cell(ws3[f"D{r}"], status)
        ws3[f"A{r}:D{r}"].font.size = 10
        ws3[f"A{r}"].row_height = 18

    ws3["A23"].value = "Note: Stress horizon of 2M satisfies Basel LCR (30 days) but is close to the 3M internal ILAAP escalation threshold."
    ws3["A23"].font.size = 9
    ws3["A23"].font.color = (89, 89, 89)
    ws3["A23"].font.italic = True

    print("Sheet 3 — Liquidity ✓")

    # ── Sheet 4: Capital ──────────────────────────────────────────────────────────
    ws4 = wb.sheets["Capital"]
    set_cols(ws4, {"A": 24, "B": 18, "C": 18, "D": 16, "E": 16, "F": 16, "G": 12})

    fmt_title(ws4["B1"], "Capital Adequacy — ICAAP Stress + 4-Year CET1 Forecast")
    fmt_subtitle(ws4["B2"], "Major European G-SIB  |  Sources: P8 (ICAAP) + P11 (Capital Forecasting)")
    ws4["A1"].row_height = 28

    # PART A — ICAAP Severe Stress Summary
    ws4["A4"].value = "PART A — ICAAP SEVERE STRESS SUMMARY  |  Scenario: +300bps / Loans -5% / Deposits -15% / CoR 100bps"
    fmt_section(ws4["A4:G4"])
    ws4["A4"].row_height = 20

    for i, h in enumerate(["METRIC", "BASE 2026F", "SEVERE STRESS",
                            "CHANGE", "THRESHOLD", "vs THRESHOLD", "STATUS"]):
        ws4[f"{'ABCDEFG'[i]}5"].value = h
    fmt_header(ws4["A5:G5"])
    ws4["A5"].row_height = 22

    icaap_rows = [
        ("NII (Eur m)",        "22,686",  "15,355",  "-7,331",   "> 75% of Base",  "67.6% of Base",  "RED"),
        ("Net Income (Eur m)", "11,194",   "2,162",  "-9,032",   "> 0",            "Positive",        "GREEN"),
        ("CET1 Ratio",         "15.88%",  "16.49%",  "+0.61pp",  "> 9.50% (MDA)", "+6.99pp",         "GREEN"),
        ("LCR",                "153.55%", "111.52%", "-42.0pp",  "> 100%",         "+11.52pp",        "GREEN"),
        ("NSFR",               "96.02%",  "85.83%",  "-10.2pp",  "> 100%",         "-14.17pp",        "RED"),
        ("EVE / Tier 1",       "13.24%",  "19.87%",  "+6.63pp",  "< 15% T1",       "+4.87pp breach",  "RED"),
    ]

    for i, (metric, base, stress, change, threshold, vs_thr, status) in enumerate(icaap_rows):
        r = 6 + i
        shade_row(ws4[f"A{r}:F{r}"], i)
        ws4[f"A{r}"].value = metric
        ws4[f"B{r}"].value = base
        ws4[f"C{r}"].value = stress
        ws4[f"D{r}"].value = change
        ws4[f"E{r}"].value = threshold
        ws4[f"F{r}"].value = vs_thr
        apply_rag_cell(ws4[f"G{r}"], status)
        ws4[f"A{r}:G{r}"].font.size = 10
        ws4[f"A{r}"].row_height = 18

    ws4["A13"].value = "Note: CET1 paradox — loan contraction (-5%) shrinks RWA faster than equity falls, so CET1 ratio improves under stress."
    ws4["A13"].font.size = 9
    ws4["A13"].font.color = (89, 89, 89)
    ws4["A13"].font.italic = True

    # PART B — 4-Year CET1 Forecast
    ws4["A15"].value = "PART B — 4-YEAR CAPITAL FORECAST  |  RWA Growth +4% p.a.  |  NI Growth +4% p.a.  |  Payout Ratio 50%"
    fmt_section(ws4["A15:G15"])
    ws4["A15"].row_height = 20

    for i, h in enumerate(["YEAR", "CET1 CAPITAL (Eur m)", "RWA (Eur m)",
                            "CET1 RATIO", "MDA BUFFER", "LEVERAGE RATIO", "RAG"]):
        ws4[f"{'ABCDEFG'[i]}16"].value = h
    fmt_header(ws4["A16:G16"])
    ws4["A16"].row_height = 22

    forecast_rows = [
        ("2025A", 109924, 724942, "15.16%", "+5.66pp", "5.29%"),
        ("2026F", 115521, 753940, "15.32%", "+5.82pp", "5.35%"),
        ("2027F", 121342, 784182, "15.47%", "+5.97pp", "5.41%"),
        ("2028F", 127396, 815749, "15.62%", "+6.12pp", "5.48%"),
        ("2029F", 133692, 848379, "15.76%", "+6.26pp", "5.54%"),
    ]

    for i, (year, cet1, rwa, cet1_pct, mda, lev) in enumerate(forecast_rows):
        r = 17 + i
        shade_row(ws4[f"A{r}:F{r}"], i)
        ws4[f"A{r}"].value = year
        ws4[f"B{r}"].value = cet1
        ws4[f"C{r}"].value = rwa
        ws4[f"D{r}"].value = cet1_pct
        ws4[f"E{r}"].value = mda
        ws4[f"F{r}"].value = lev
        apply_rag_cell(ws4[f"G{r}"], "GREEN")
        ws4[f"A{r}:G{r}"].font.size = 10
        ws4[f"A{r}"].row_height = 18

    ws4["A23"].value = "Note: RWA treadmill absorbs 78.6% of retained earnings. Only 21.4% is true organic buffer build. MDA threshold = 9.50% (P1 4.50% + CCoB 2.50% + G-SIB 1.00% + P2R 1.50%)."
    ws4["A23"].font.size = 9
    ws4["A23"].font.color = (89, 89, 89)
    ws4["A23"].font.italic = True

    print("Sheet 4 — Capital ✓")

    # ── Sheet 5: Market Risk ──────────────────────────────────────────────────────
    ws5 = wb.sheets["Market Risk"]
    set_cols(ws5, {"A": 22, "B": 18, "C": 18, "D": 18, "E": 18, "F": 16, "G": 14})

    fmt_title(ws5["B1"], "Market Risk — Bond Portfolio & Yield Curve")
    fmt_subtitle(ws5["B2"], "Major European G-SIB  |  Sources: P4 (Bond Portfolio) + P5 (Yield Curve Bootstrap)")
    ws5["A1"].row_height = 28

    # PART A — Portfolio Summary + DV01 by Bond
    ws5["A4"].value = "PART A — SECURITIES PORTFOLIO  |  Total = Eur 153,107m  |  DV01 = Eur 100.88m per bp"
    fmt_section(ws5["A4:G4"])
    ws5["A4"].row_height = 20

    for i, h in enumerate(["BOND", "TYPE", "NOTIONAL (Eur m)",
                            "MOD. DURATION", "DV01 (Eur m/bp)", "DV01 SHARE (%)", "STATUS"]):
        ws5[f"{'ABCDEFG'[i]}5"].value = h
    fmt_header(ws5["A5:G5"])
    ws5["A5"].row_height = 22

    bond_rows = [
        ("ES Bono 30Y",   "Government",     15237, 19.23, 29.29, 29.0),
        ("IT BTP 10Y",    "Government",     30000,  8.60, 25.79, 25.6),
        ("FR OAT 5Y",     "Government",     40000,  4.60, 18.39, 18.2),
        ("Corp IG 10Y",   "Corporate",      10621,  8.35,  8.88,  8.8),
        ("Corp IG 7Y",    "Corporate",      12000,  6.16,  7.39,  7.3),
        ("DE Bund 2Y",    "Government",     25000,  1.93,  4.82,  4.8),
        ("Corp IG 3Y",    "Corporate",      10000,  2.88,  2.88,  2.9),
        ("Covered 5Y",    "Covered Bond",    4686,  4.71,  2.21,  2.2),
        ("EIB Supra 5Y",  "Supranational",   1063,  4.68,  0.50,  0.5),
        ("Covered 2Y",    "Covered Bond",    4500,  1.93,  0.87,  0.9),
        ("PORTFOLIO",     "",              153107,  6.59, 100.88, 100.0),
    ]

    for i, (bond, btype, notional, dur, dv01, share) in enumerate(bond_rows):
        r = 6 + i
        shade_row(ws5[f"A{r}:F{r}"], i)
        ws5[f"A{r}"].value = bond
        ws5[f"B{r}"].value = btype
        ws5[f"C{r}"].value = notional
        ws5[f"D{r}"].value = f"{dur:.2f}y"
        ws5[f"E{r}"].value = dv01
        ws5[f"F{r}"].value = f"{share:.1f}%"
        ws5[f"G{r}"].value = ""
        ws5[f"A{r}:G{r}"].font.size = 10
        ws5[f"A{r}"].row_height = 18
        if bond == "PORTFOLIO":
            ws5[f"A{r}:G{r}"].font.bold = True

    # PART B — Rate Shock P&L
    ws5["A18"].value = "PART B — RATE SHOCK P&L  |  Exact Full Reprice  |  Convexity Benefit at +200bps = Eur 2,276m"
    fmt_section(ws5["A18:G18"])
    ws5["A18"].row_height = 20

    for i, h in enumerate(["RATE SHOCK", "EXACT P&L (Eur m)", "DUR. ESTIMATE (Eur m)",
                            "CONVEXITY BENEFIT (Eur m)", "P&L / PORTFOLIO (%)", "STATUS"]):
        ws5[f"{'ABCDEF'[i]}19"].value = h
    fmt_header(ws5["A19:F19"])
    ws5["A19"].row_height = 22

    pnl_rows = [
        ("-200 bps", 23200,  -20176, 0,     "+15.2%",  "GREEN"),
        ("-100 bps", 10800,  -10088, 0,     "+7.1%",   "GREEN"),
        (" -50 bps",  5200,   -5044, 0,     "+3.4%",   "GREEN"),
        (" +50 bps", -4900,    5044, 144,   "-3.2%",   "GREEN"),
        ("+100 bps", -9500,   10088, 588,   "-6.2%",   "GREEN"),
        ("+200 bps",-17900,   20176, 2276,  "-11.7%",  "GREEN"),
    ]

    for i, (shock, exact, dur_est, conv, pct, status) in enumerate(pnl_rows):
        r = 20 + i
        shade_row(ws5[f"A{r}:E{r}"], i)
        ws5[f"A{r}"].value = shock
        ws5[f"B{r}"].value = exact
        ws5[f"C{r}"].value = dur_est
        ws5[f"D{r}"].value = conv if conv > 0 else "-"
        ws5[f"E{r}"].value = pct
        apply_rag_cell(ws5[f"F{r}"], status)
        ws5[f"A{r}:F{r}"].font.size = 10
        ws5[f"A{r}"].row_height = 18

    # PART C — Yield Curve Snapshot
    ws5["A27"].value = "PART C — EUR YIELD CURVE SNAPSHOT  |  2026F  |  Bootstrapped from ECB DFR + Euribor + Swap Rates"
    fmt_section(ws5["A27:G27"])
    ws5["A27"].row_height = 20

    for i, h in enumerate(["TENOR", "PAR RATE", "SPOT RATE", "DISCOUNT FACTOR", "CURVE FEATURE"]):
        ws5[f"{'ABCDE'[i]}28"].value = h
    fmt_header(ws5["A28:E28"])
    ws5["A28"].row_height = 22

    curve_rows = [
        ("ECB DFR (O/N)", "2.25%",   "2.25%",  "1.00000", "Short-end anchor"),
        ("3M Euribor",    "2.35%",   "2.35%",  "0.99413", ""),
        ("1Y",            "2.4053%", "2.4053%","0.97651",  ""),
        ("2Y",            "2.4789%", "2.5106%","0.95219",  ""),
        ("5Y",            "2.7000%", "2.8589%","0.87493",  "Swap anchor"),
        ("7Y",            "2.6400%", "2.8602%","0.83318",  "Curve peak"),
        ("10Y",           "2.5500%", "2.8535%","0.77800",  "Slight inversion 5Y-10Y"),
    ]

    for i, (tenor, par, spot, df, note) in enumerate(curve_rows):
        r = 29 + i
        shade_row(ws5[f"A{r}:E{r}"], i)
        ws5[f"A{r}"].value = tenor
        ws5[f"B{r}"].value = par
        ws5[f"C{r}"].value = spot
        ws5[f"D{r}"].value = df
        ws5[f"E{r}"].value = note
        ws5[f"A{r}:E{r}"].font.size = 10
        ws5[f"A{r}"].row_height = 18

    print("Sheet 5 — Market Risk ✓")

    # PART A — Portfolio Summary + DV01 by Bond
    ws5["A4"].value = "PART A — SECURITIES PORTFOLIO  |  Total = Eur 153,107m  |  DV01 = Eur 100.88m per bp"
    fmt_section(ws5["A4:G4"])
    ws5["A4"].row_height = 20

    for i, h in enumerate(["BOND", "TYPE", "NOTIONAL (Eur m)",
                            "MOD. DURATION", "DV01 (Eur m/bp)", "DV01 SHARE (%)", ""]):
        ws5[f"{'ABCDEFG'[i]}5"].value = h
    fmt_header(ws5["A5:G5"])
    ws5["A5"].row_height = 22

    bond_rows = [
        ("ES Bono 30Y",  "Government",    15237, 19.23, 29.29, 29.0),
        ("IT BTP 10Y",   "Government",    30000,  8.60, 25.79, 25.6),
        ("FR OAT 5Y",    "Government",    40000,  4.60, 18.39, 18.2),
        ("Corp IG 10Y",  "Corporate",     10621,  8.35,  8.88,  8.8),
        ("Corp IG 7Y",   "Corporate",     12000,  6.16,  7.39,  7.3),
        ("DE Bund 2Y",   "Government",    25000,  1.93,  4.82,  4.8),
        ("Corp IG 3Y",   "Corporate",     10000,  2.88,  2.88,  2.9),
        ("Covered 5Y",   "Covered Bond",   4686,  4.71,  2.21,  2.2),
        ("EIB Supra 5Y", "Supranational",  1063,  4.68,  0.50,  0.5),
        ("Covered 2Y",   "Covered Bond",   4500,  1.93,  0.87,  0.9),
        ("PORTFOLIO",    "",             153107,  6.59, 100.88, 100.0),
    ]

    for i, (bond, btype, notional, dur, dv01, share) in enumerate(bond_rows):
        r = 6 + i
        shade_row(ws5[f"A{r}:F{r}"], i)
        ws5[f"A{r}"].value = bond
        ws5[f"B{r}"].value = btype
        ws5[f"C{r}"].value = notional
        ws5[f"D{r}"].value = f"{dur:.2f}y"
        ws5[f"E{r}"].value = dv01
        ws5[f"F{r}"].value = f"{share:.1f}%"
        ws5[f"A{r}:F{r}"].font.size = 10
        ws5[f"A{r}"].row_height = 18
        if bond == "PORTFOLIO":
            ws5[f"A{r}:F{r}"].font.bold = True

    print("Part 1 done ✓")

    # PART B — Rate Shock P&L
    ws5["A18"].value = "PART B — RATE SHOCK P&L  |  Exact Full Reprice  |  Convexity Benefit at +200bps = Eur 2,276m"
    fmt_section(ws5["A18:F18"])
    ws5["A18"].row_height = 20

    for i, h in enumerate(["RATE SHOCK", "EXACT P&L (Eur m)", "DUR. ESTIMATE (Eur m)",
                            "CONVEXITY BENEFIT (Eur m)", "P&L / PORTFOLIO (%)", "STATUS"]):
        ws5[f"{'ABCDEF'[i]}19"].value = h
    fmt_header(ws5["A19:F19"])
    ws5["A19"].row_height = 22

    pnl_rows = [
        ("-200 bps",  23200, -20176,    0, "+15.2%", "GREEN"),
        ("-100 bps",  10800, -10088,    0,  "+7.1%", "GREEN"),
        (" -50 bps",   5200,  -5044,    0,  "+3.4%", "GREEN"),
        (" +50 bps",  -4900,   5044,  144,  "-3.2%", "GREEN"),
        ("+100 bps",  -9500,  10088,  588,  "-6.2%", "GREEN"),
        ("+200 bps", -17900,  20176, 2276, "-11.7%", "GREEN"),
    ]

    for i, (shock, exact, dur_est, conv, pct, status) in enumerate(pnl_rows):
        r = 20 + i
        shade_row(ws5[f"A{r}:E{r}"], i)
        ws5[f"A{r}"].value = shock
        ws5[f"B{r}"].value = exact
        ws5[f"C{r}"].value = dur_est
        ws5[f"D{r}"].value = conv if conv > 0 else "-"
        ws5[f"E{r}"].value = pct
        apply_rag_cell(ws5[f"F{r}"], status)
        ws5[f"A{r}:F{r}"].font.size = 10
        ws5[f"A{r}"].row_height = 18

    # PART C — Yield Curve Snapshot
    ws5["A27"].value = "PART C — EUR YIELD CURVE SNAPSHOT  |  2026F  |  ECB DFR 2.25% + 3M Euribor 2.35% + 5Y Swap 2.70% + 10Y Swap 2.55%"
    fmt_section(ws5["A27:F27"])
    ws5["A27"].row_height = 20

    for i, h in enumerate(["TENOR", "PAR RATE", "SPOT RATE", "DISCOUNT FACTOR", "CURVE FEATURE"]):
        ws5[f"{'ABCDE'[i]}28"].value = h
    fmt_header(ws5["A28:E28"])
    ws5["A28"].row_height = 22

    curve_rows = [
        ("ECB DFR (O/N)", "2.25%",    "2.25%",   "1.00000", "Short-end anchor"),
        ("3M Euribor",    "2.35%",    "2.35%",   "0.99413", ""),
        ("1Y",            "2.4053%",  "2.4053%", "0.97651",  ""),
        ("2Y",            "2.4789%",  "2.5106%", "0.95219",  ""),
        ("5Y",            "2.7000%",  "2.8589%", "0.87493",  "Swap anchor"),
        ("7Y",            "2.6400%",  "2.8602%", "0.83318",  "Curve peak"),
        ("10Y",           "2.5500%",  "2.8535%", "0.77800",  "Slight inversion 5Y-10Y"),
    ]

    for i, (tenor, par, spot, df, note) in enumerate(curve_rows):
        r = 29 + i
        shade_row(ws5[f"A{r}:E{r}"], i)
        ws5[f"A{r}"].value = tenor
        ws5[f"B{r}"].value = par
        ws5[f"C{r}"].value = spot
        ws5[f"D{r}"].value = df
        ws5[f"E{r}"].value = note
        ws5[f"A{r}:E{r}"].font.size = 10
        ws5[f"A{r}"].row_height = 18

    print("Sheet 5 — Market Risk ✓")

    # ── Sheet 6: FTP & Behavioural ────────────────────────────────────────────────
    ws6 = wb.sheets["FTP & Behavioural"]
    set_cols(ws6, {"A": 22, "B": 18, "C": 18, "D": 16, "E": 16, "F": 16, "G": 14})

    fmt_title(ws6["B1"], "FTP & Behavioural — Funds Transfer Pricing + CPR Model")
    fmt_subtitle(ws6["B2"], "Major European G-SIB  |  Sources: P6 (FTP Framework) + P7 (CPR Behavioural Model)")
    ws6["A1"].row_height = 28

    # PART A — FTP Curve
    ws6["A4"].value = "PART A — FTP CURVE  |  8 Tenors  |  Base Rate + Liquidity Premium"
    fmt_section(ws6["A4:G4"])
    ws6["A4"].row_height = 20

    for i, h in enumerate(["TENOR", "BASE RATE", "LIQ. PREMIUM (bps)",
                            "FTP RATE", "SOURCE", ""]):
        ws6[f"{'ABCDEF'[i]}5"].value = h
    fmt_header(ws6["A5:F5"])
    ws6["A5"].row_height = 22

    ftp_curve = [
        ("Overnight", "2.2500%",  "0 bps",  "2.2500%", "ECB DFR"),
        ("1 Month",   "2.2826%",  "5 bps",  "2.3326%", "Interpolated"),
        ("3 Months",  "2.3500%", "10 bps",  "2.4500%", "3M Euribor"),
        ("6 Months",  "2.3684%", "15 bps",  "2.5184%", "Interpolated"),
        ("1 Year",    "2.4053%", "20 bps",  "2.6053%", "Bootstrap 1Y"),
        ("2 Year",    "2.5106%", "25 bps",  "2.7606%", "Bootstrap 2Y"),
        ("5 Year",    "2.8589%", "35 bps",  "3.2089%", "Bootstrap 5Y"),
        ("10 Year",   "2.8535%", "50 bps",  "3.3535%", "Bootstrap 10Y"),
    ]

    for i, (tenor, base, liq, ftp, source) in enumerate(ftp_curve):
        r = 6 + i
        shade_row(ws6[f"A{r}:E{r}"], i)
        ws6[f"A{r}"].value = tenor
        ws6[f"B{r}"].value = base
        ws6[f"C{r}"].value = liq
        ws6[f"D{r}"].value = ftp
        ws6[f"E{r}"].value = source
        ws6[f"A{r}:E{r}"].font.size = 10
        ws6[f"A{r}"].row_height = 18

    # PART B — FTP NII Attribution
    ws6["A15"].value = "PART B — FTP NII ATTRIBUTION  |  Total NII = Eur 23,975m  |  Cross-check vs Excel = Eur 0"
    fmt_section(ws6["A15:G15"])
    ws6["A15"].row_height = 20

    for i, h in enumerate(["DESK", "PRODUCT RATE", "FTP RATE",
                            "NET MARGIN", "BALANCE (Eur m)", "NII (Eur m)", "SHARE"]):
        ws6[f"{'ABCDEFG'[i]}16"].value = h
    fmt_header(ws6["A16:G16"])
    ws6["A16"].row_height = 22

    ftp_nii = [
        ("Mortgage Desk",  "4.50%", "3.2089%", "1.2911%", 277284,  3580, "14.9%"),
        ("Deposit Desk",   "0.40%", "2.2500%", "1.8500%", 1102453, 20395, "85.1%"),
        ("TOTAL",          "",      "",         "",        1379737, 23975, "100%"),
    ]

    for i, (desk, prod, ftp, margin, bal, nii, share) in enumerate(ftp_nii):
        r = 17 + i
        shade_row(ws6[f"A{r}:F{r}"], i)
        ws6[f"A{r}"].value = desk
        ws6[f"B{r}"].value = prod
        ws6[f"C{r}"].value = ftp
        ws6[f"D{r}"].value = margin
        ws6[f"E{r}"].value = bal
        ws6[f"F{r}"].value = nii
        ws6[f"G{r}"].value = share
        ws6[f"A{r}:G{r}"].font.size = 10
        ws6[f"A{r}"].row_height = 18
        if desk == "TOTAL":
            ws6[f"A{r}:G{r}"].font.bold = True

    # PART C — CPR NII Grid
    ws6["A21"].value = "PART C — CPR BEHAVIOURAL MODEL  |  NII Impact Grid  |  Tier 1 = Eur 132,173m"
    fmt_section(ws6["A21:G21"])
    ws6["A21"].row_height = 20

    for i, h in enumerate(["SCENARIO", "RATE DELTA", "CPR MULTIPLIER",
                            "EFF. CPR", "NII IMPACT (Eur m)", "EVE / T1 (%)", "STATUS"]):
        ws6[f"{'ABCDEFG'[i]}22"].value = h
    fmt_header(ws6["A22:G22"])
    ws6["A22"].row_height = 22

    cpr_rows = [
        ("Base",       "-0.225%", "x1.0", "10.0%",  -208,  13.24, "GREEN"),
        ("Rate Hike",  "+1.575%", "x0.5",  "5.0%",  +728,  12.85, "GREEN"),
        ("Rate Cut",   "-2.025%", "x1.5", "15.0%", -2808,  12.45, "GREEN"),
        ("Stress",     "+2.475%", "x2.0", "20.0%", +4575,  12.05, "GREEN"),
    ]

    for i, (scenario, delta, mult, eff_cpr, nii, eve_t1, status) in enumerate(cpr_rows):
        r = 23 + i
        shade_row(ws6[f"A{r}:F{r}"], i)
        ws6[f"A{r}"].value = scenario
        ws6[f"B{r}"].value = delta
        ws6[f"C{r}"].value = mult
        ws6[f"D{r}"].value = eff_cpr
        ws6[f"E{r}"].value = nii
        ws6[f"F{r}"].value = f"{eve_t1:.2f}%"
        apply_rag_cell(ws6[f"G{r}"], status)
        ws6[f"A{r}:G{r}"].font.size = 10
        ws6[f"A{r}"].row_height = 18

    ws6["A28"].value = "Note: Rate Cut is worst NII scenario (CPR x1.5 amplifies reinvestment loss). All EVE ratios below 15% T1 — 55% IRS hedge effective."
    ws6["A28"].font.size = 9
    ws6["A28"].font.color = (89, 89, 89)
    ws6["A28"].font.italic = True

    print("Sheet 6 — FTP & Behavioural ✓")

    # ── Save and close ────────────────────────────────────────────────────────
    save_path = SAVE_PATH
    wb.save(save_path)
    print(f"Saved: {save_path}")
    print("Dashboard refresh complete ✓")

except Exception as e:
    print(f"ERROR during refresh: {e}")
    raise
finally:
    try:
        wb.close()
        app.quit()
    except Exception:
        pass
