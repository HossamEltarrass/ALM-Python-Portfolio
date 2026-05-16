# =============================================================================
# data.py — ALM Dashboard Capstone (Project 12)
# Major European G-SIB | 2025A / 2026F
# =============================================================================
# PURPOSE:
#   This file holds ALL verified headline numbers from Projects 1–11 as
#   Python dictionaries. dashboard.py imports this file and writes the data
#   to Excel via xlwings. Do NOT edit numbers here unless you re-run the
#   source project and get a new verified cross-check.
#
# CONVENTION:
#   All monetary values are in €millions (€m) unless labelled otherwise.
#   All percentages are floats (e.g. 15.16 means 15.16%, not 0.1516).
# =============================================================================

# ---------------------------------------------------------------------------
# P1 — NII Scenario Tool
# Source: NII_Scenario_Tool.ipynb | Base NII cross-check = 0.0 vs Excel
# ---------------------------------------------------------------------------
P1 = {
    "project":          "P1 — NII Scenario Tool",
    "section":          "Section 1",
    "base_nii":         22_085,     # €m — Base (0bp shock, deposit beta 0.40)
    "hike_nii":         23_676,     # €m — Rate Hike +200bps
    "cut_nii":          16_192,     # €m — Rate Cut −200bps  ← WORST CASE
    "stress_nii":       21_245,     # €m — Stress +300bps
    "worst_scenario":   "Rate Cut −200bps",
    "worst_delta_nii":  -5_893,     # €m — change vs Base under worst scenario
}

# ---------------------------------------------------------------------------
# P2 — IRRBB Stress Testing (Basel ΔEVE)
# Source: IRRBB_Stress_Testing.ipynb | Cross-check €0.3m rounding only
# Tier 1 used in P2: €80,000m proxy (before full equity model)
# ---------------------------------------------------------------------------
P2 = {
    "project":              "P2 — IRRBB Stress Testing",
    "section":              "Sections 2–3",
    "tier1_capital":        80_000,     # €m — Tier 1 proxy used in P2
    "worst_scenario":       "Parallel Up +200bps",
    "worst_delta_eve":      -22_345,    # €m — ΔEVE under worst Basel scenario
    "worst_eve_pct_t1":     27.9,       # % of Tier 1 — OUTLIER (threshold = 15%)
    "best_delta_nii":       9_582,      # €m — Short Rate Up +250bps
    "worst_delta_nii":      -6_516,     # €m — Parallel Down −200bps
    "outlier":              True,       # All 6 scenarios breach 15% threshold
}

# ---------------------------------------------------------------------------
# P3 — LCR / NSFR Calculator (Basel III Liquidity)
# Source: LCR_NSFR_Calculator.ipynb | Cross-check: LCR −0.01%, NSFR 0.00%
# ---------------------------------------------------------------------------
P3 = {
    "project":          "P3 — LCR / NSFR Calculator",
    "section":          "Sections 8–9",
    "base_lcr":         153.4,      # % — Base scenario (threshold = 100%)
    "stress_lcr":       148.3,      # % — Stress scenario (passes)  # Stress scenario LCR — NOT base LCR
    "base_nsfr":        102.2,      # % — Base scenario (threshold = 100%)
    "stress_nsfr":      99.8,       # % — Stress scenario ← BREACH
    "hqla_eur_m":       364_437,    # €m — High Quality Liquid Assets (Level 1+2A)
    "nsfr_breach":      True,       # Stress NSFR breaches 100% threshold
    "binding_risk":     "NSFR",     # LCR passes all scenarios; NSFR is binding
}

# ---------------------------------------------------------------------------
# P4 — Bond Pricing & Duration (Fixed Income Sensitivity)
# Source: Bond_Pricing_Duration.ipynb | 10-bond €153,107m securities portfolio
# ---------------------------------------------------------------------------
P4 = {
    "project":              "P4 — Bond Pricing & Duration",
    "section":              "Section 5",
    "portfolio_eur_m":      153_107,    # €m — Total securities portfolio
    "portfolio_dv01":       100.88,     # €m per basis point
    "wtd_mod_duration":     6.59,       # years
    "wtd_convexity":        85.38,      # dimensionless
    "loss_200bps_eur_m":    -17_900,    # €m — P&L impact at +200bps (exact reprice)
    "convexity_benefit":    2_276,      # €m — convexity saves vs duration-only estimate
    "gain_neg200bps":       23_200,     # €m — P&L impact at −200bps (asymmetry = convexity)
}

# ---------------------------------------------------------------------------
# P5 — Yield Curve Bootstrap (EUR Zero Curve)
# Source: Yield_Curve_Bootstrap.ipynb | 4 inputs → 10Y annual spot curve
# ---------------------------------------------------------------------------
P5 = {
    "project":          "P5 — Yield Curve Bootstrap",
    "section":          "YieldCurve sheet",
    "ecb_dfr":          2.25,       # % — ECB Deposit Facility Rate (2026F)
    "euribor_3m":       2.35,       # % — 3M Euribor (2026F)
    "swap_5y":          2.70,       # % — 5Y EUR Swap Rate (2026F)
    "swap_10y":         2.55,       # % — 10Y EUR Swap Rate (2026F)
    "spot_1y":          2.4053,     # % — Bootstrapped 1Y spot rate
    "spot_5y":          2.8589,     # % — Bootstrapped 5Y spot rate (peak)
    "spot_10y":         2.8535,     # % — Bootstrapped 10Y spot rate
    "curve_shape":      "Hump-shaped",  # Peaks ~7Y (2.860%), slight inversion 5Y→10Y
}

# ---------------------------------------------------------------------------
# P6 — FTP Framework (Funds Transfer Pricing)
# Source: P6_ftp_framework.ipynb | Section 15 | Cross-check €0–€0.4m rounding
# ---------------------------------------------------------------------------
P6 = {
    "project":          "P6 — FTP Framework",
    "section":          "Section 15",
    "mortgage_nii":     3_580,      # €m — Mortgage desk NII (5Y FTP matched)
    "deposit_nii":      20_395,     # €m — Retail deposit desk NII (O/N FTP matched)
    "total_ftp_nii":    23_975,     # €m — Combined two-desk NII
    "mortgage_nim":     1.2911,     # % — Net interest margin on mortgage book
    "deposit_margin":   1.85,       # % — Franchise margin on retail deposits
    "ftp_rate_5y":      3.2089,     # % — 5Y FTP charge (base + 35bps liq. premium)
}

# ---------------------------------------------------------------------------
# P7 — CPR / Behavioural Model (Prepayment)
# Source: P7_CPR_Behavioral_Model.ipynb | Section 16 | Cross-check diff = 0.000
# ---------------------------------------------------------------------------
P7 = {
    "project":              "P7 — CPR Behavioural Model",
    "section":              "Section 16",
    "base_nii_impact":      -208,       # €m — Base (CPR=10%, ECB drift drag)
    "hike_nii_impact":      728,        # €m — Rate Hike (reinvest at higher yield)
    "cut_nii_impact":       -2_808,     # €m — Rate Cut ← WORST NII scenario
    "stress_nii_impact":    4_575,      # €m — Stress (best NII — distressed prepay)
    "eve_cpr0_eur_m":       17_506,     # €m — Net EVE at CPR=0% (worst EVE case)
    "eve_cpr0_t1_pct":      13.24,      # % of Tier 1 — within 15% threshold
    "hedge_ratio":          0.55,       # 55% IRS overlay applied
}

# ---------------------------------------------------------------------------
# P8 — ICAAP Stress Testing (Severe Stress)
# Source: P8_ICAAP_Stress_Testing.ipynb | Section 17
# Stress scenario: +300bps / −5% loans / −15% deposits / CoR 100bps / beta 0.60
# ---------------------------------------------------------------------------
P8 = {
    "project":              "P8 — ICAAP Stress Testing",
    "section":              "Section 17",
    # NII
    "base_nii":             22_686,     # €m — 2026F Base NII
    "stress_nii":           15_355,     # €m — Severe stress NII  ← RED
    # Net Income
    "base_net_income":      11_194,     # €m — 2026F Base
    "stress_net_income":    2_162,      # €m — Severe stress (GREEN — still positive)
    # CET1
    "base_cet1":            15.88,      # % — 2026F Base
    "stress_cet1":          16.49,      # % — Severe stress (GREEN — paradox: RWA shrinks)
    # Liquidity
    "base_lcr":             153.55,     # % — 2026F Base
    "stress_lcr":           111.52,     # % — Severe stress (GREEN)
    "base_nsfr":            96.02,      # % — 2026F Base  # 2026F ICAAP base (differs from P3 2025A base of 102.2%)
    "stress_nsfr":          85.83,      # % — Severe stress  ← RED (< 100%)
    # EVE
    "stress_eve_t1_pct":    19.87,      # % of Tier 1  ← RED (> 15% threshold)
    "red_flags":            3,          # Number of RED metrics: NII, NSFR, EVE
}

# ---------------------------------------------------------------------------
# P9 — Hedge Effectiveness (IRS Overlay)
# Source: P9_Hedge_Effectiveness.ipynb | Section 18
# Cross-check: all 18 cells diff < €0.005m (rounding only)
# ---------------------------------------------------------------------------
P9 = {
    "project":              "P9 — Hedge Effectiveness",
    "section":              "Section 18",
    "tier1_capital":        132_173,    # €m — actual Tier 1 (Projects 7–11)
    "hedge_ratio":          0.55,       # 55% IRS overlay
    "worst_scenario":       "Par Up +200bps",
    "gross_eve_worst":      38_901.86,  # €m — unhedged EVE exposure
    "hedge_offset_worst":   21_396.02,  # €m — IRS overlay absorbs
    "net_eve_worst":        17_505.84,  # €m — residual after hedge
    "net_eve_t1_pct":       13.24,      # % of Tier 1 — within 15% threshold ✓
    "unhedged_t1_pct":      29.4,       # % — gross EVE/T1 without hedge (outlier)
    "all_within_limit":     True,       # All 6 Basel scenarios pass after hedge
}

# ---------------------------------------------------------------------------
# P10 — Monthly NII & Maturity Ladder
# Source: Monthly_NII_Maturity_Ladder.ipynb | Sections 12 & 13
# Cross-check: Base monthly NII sum = €22,085m (matches P1 annual NII) ✅
# ---------------------------------------------------------------------------
P10 = {
    "project":                      "P10 — Monthly NII & Maturity Ladder",
    "section":                      "Sections 12–13",
    "monthly_nii_annual_sum":       22_085,     # €m — matches P1 exactly (cross-check)
    "base_survival_months":         9,          # months — base scenario liquidity horizon
    "stress_survival_months":       2,          # months — stress scenario ← only 2M
    "hqla_eur_m":                   364_437,    # €m — HQLA buffer (same as P3)
    "repo_dependency_eur_m":        357_947,    # €m — key liquidity vulnerability
    "asset_sensitive":              True,       # Rate hike increases NII more than cut reduces it
}

# ---------------------------------------------------------------------------
# P11 — Capital Forecasting (4-Year 2026F–2029F)
# Source: P11_Capital_Forecasting.ipynb | Section 7
# All 10 cross-checks passed ✅
# ---------------------------------------------------------------------------
P11 = {
    "project":              "P11 — Capital Forecasting",
    "section":              "Section 7",
    # Starting point (2025A actuals)
    "cet1_2025a_pct":       15.74,      # %
    "mda_buffer_2025a_pp":  6.24,       # percentage points above MDA threshold
    "leverage_2025a_pct":   5.29,       # % — Tier 1 leverage ratio
    # End of forecast (2029F)
    "cet1_2029f_pct":       16.26,      # %
    "mda_buffer_2029f_pp":  6.76,       # pp — buffer widens modestly
    "leverage_2029f_pct":   5.54,       # %
    # Capital generation (4-year cumulative)
    "cumulative_net_income":    47_535, # €m — 4 years
    "cumulative_retained":      23_768, # €m — 50% payout ratio
    "rwa_absorption_pct":       78.6,   # % of retained earnings consumed by RWA growth
    "organic_build_pct":        21.4,   # % of retained earnings as true buffer build
    "all_rag_green":            True,   # All years 2026F–2029F = GREEN
}

# ---------------------------------------------------------------------------
# Convenience: ordered list for looping in dashboard.py
# ---------------------------------------------------------------------------
ALL_PROJECTS = [P1, P2