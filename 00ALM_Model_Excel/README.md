# Major European G-SIB — ALM Master Model

![Version](https://img.shields.io/badge/Version-v10-darkgreen)
![Framework](https://img.shields.io/badge/Framework-Basel%20III%20%2F%20CRR2%20%2F%20EBA%2FGL%2F2022%2F14-darkgreen)
![Currency](https://img.shields.io/badge/Currency-EUR%20millions-darkgreen)
![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-darkgreen)
![Updated](https://img.shields.io/badge/Updated-May%202026-darkgreen)

---

A bank-level Asset-Liability Management model built from scratch — no templates, no shortcuts. Calibrated to Q4 2025 Pillar 3 disclosures of a major European G-SIB, it replicates the full ALCO analytical cycle that treasury teams at large banks run every quarter: balance sheet forecasting, NII simulation, IRRBB stress testing, liquidity risk, and capital planning — all in one interconnected workbook, across four rate scenarios, over a three-year horizon.

The model is formula-driven throughout. One dropdown on the Dashboard propagates across 18 analytical sections and 1,000+ formulas with no macros, no VBA, and no manual recalculation. Every regulatory parameter carries an inline citation to the EBA guideline or CRR article it implements.

> This is the analytical engine behind the [ALM Python Portfolio](https://github.com/HossamEltarrass/ALM-Python-Portfolio) — 12 Python projects that replicate, extend, and automate each section of this model in code.

---

## Workbook Architecture

| Sheet | Role |
|---|---|
| **Cover** | Model metadata, architecture overview, key metrics snapshot, author card |
| **Dashboard** | Executive ALCO view — live scenario selector, KPI cards, balance sheet forecast, profitability, liquidity ratios, IRRBB summary, four-scenario comparison |
| **Engine** | Central control layer — rate curve, scenario inputs, behavioural parameters, regulatory thresholds; all CHOOSE-based propagation lives here |
| **Model** | Full analytical engine — 18 modular sections, 1,000+ formulas, every regulatory calculation |
| **YieldCurve** | EUR spot rate bootstrap (4 market inputs → 10Y annual curve) + 6 EBA/GL/2022/14 IRRBB shock scenarios |
| **Master Balance Sheet** | Source-of-truth — Q4 2024A and Q4 2025A actuals, colour-coded for HQLA eligibility and RSF treatment |

---

## Four Scenarios

| # | Scenario | Rate Shock | Loan Growth | Deposit Growth | What It Tests |
|---|---|---|---|---|---|
| 1 | **Base** | — | +3.0% | +2.5% | Steady-state profitability |
| 2 | **Rate Hike** | +200bps | +2.0% | +2.0% | NII upside, EVE stress |
| 3 | **Rate Cut** | −200bps | +4.0% | +3.0% | NIM compression, deposit repricing |
| 4 | **Stress** | +300bps | +1.0% | 0% | Severe combined shock, capital adequacy |

Switch scenario via a single dropdown on the Dashboard — all 18 sections update instantly.

---

## Key Outputs — Base Scenario (2026F)

| Metric | Value | Threshold | Status |
|---|---|---|---|
| Net Interest Income | **€22.69bn** | — | — |
| Net Interest Margin | **1.74%** | EWI >5% NII | ✅ PASS |
| CET1 Ratio | **15.88%** | ≥ 13.5% (P1+P2R+CCyB) | ✅ PASS |
| Leverage Ratio | **4.82%** | ≥ 3.0% | ✅ PASS |
| LCR | **1.54x** | ≥ 1.00x | ✅ PASS |
| NSFR | **0.96x** | ≥ 1.00x | ⚠️ BREACH (intentional — stress scenario NMD haircut) |
| EVE / Tier 1 Capital | **13.2%** | < 15% outlier threshold | ✅ PASS |

> **On the NSFR breach:** The base scenario NSFR of 0.96x reflects the conservative NMD behavioural assumptions applied (EBA/GL/2022/14 Table 2 caps, 70% core / 30% non-core split). This is a deliberate modelling choice to reflect a realistic stressed funding profile rather than an optimistic one. It is flagged in the model's RAG scorecard as a monitoring item.

---

## The 18 Model Sections

Each section is modular — it reads from the Engine and writes to the Dashboard. Changing the scenario on the Dashboard cascades through all 18 simultaneously.

### Interest Income & Profitability
| Section | What It Calculates | What Decision It Informs |
|---|---|---|
| **1 — NII Simulation** | Asset and liability interest income/expense by line, base year 2025A | Validates the model against actuals; anchors the forecast |
| **2 — P&L Model** | Full income statement 2025A → 2028F (NII, fees, OpEx, provisions, net income) | Forward earnings trajectory; dividend capacity; retained earnings path |
| **8 — NIM Trend** | Net interest margin 2024A → 2028F | Structural margin evolution; pricing strategy signal |
| **11 — NIM Sensitivity** | NIM grid vs ECB rate × deposit beta | How sensitive NII is to the speed of deposit repricing |
| **12 — Monthly NII** | 12-month forward NII simulation, EBA/GL/2022/14 | Short-term NII early warning indicator; supervisory trigger check |

### Interest Rate Risk (IRRBB)
| Section | What It Calculates | What Decision It Informs |
|---|---|---|
| **3 — Repricing Gap** | Asset/liability gap by time bucket, ΔNii per 100bps | Where rate sensitivity is concentrated across the maturity profile |
| **4 — IRRBB Summary** | NII and EVE impact under 6 Basel shock scenarios | Outlier test pass/fail; hedging need identification |
| **14 — PVBP / DV01** | Duration-weighted EVE, EBA/GL/2022/14 Annex II | Interest rate risk capital charge estimation |
| **14b — EVE Full CF** | Full cashflow discounting, CRR Art. 448 Pillar 3 method | Regulatory EVE disclosure; comparison with simplified method |

### Liquidity
| Section | What It Calculates | What Decision It Informs |
|---|---|---|
| **5 — LCR** | HQLA, 30-day stress outflows/inflows, Del. Reg. (EU) 2022/786 | Short-term liquidity adequacy; HQLA buffer sizing |
| **6 — NSFR** | ASF and RSF by instrument, CRR Art. 428a–428at | Structural funding stability; long-term funding gap |
| **13 — Maturity Ladder** | Cumulative liquidity gap, survival horizon, EBA/GL/2024/35 | How long the bank can survive without market access |

### Capital & Regulatory
| Section | What It Calculates | What Decision It Informs |
|---|---|---|
| **7 — Capital** | RWA, CET1 ratio, leverage ratio, MDA buffer, CRR Art. 92 | Capital adequacy trajectory; distribution constraint |
| **9 — Regulatory RAG** | Traffic-light dashboard for all key ratios, 2025A–2028F | Board-level summary; regulatory breach early warning |
| **10 — Scenario Comparison** | All four scenarios side-by-side, delta vs Base | Strategic rate sensitivity; hedging and pricing decisions |

---

## Regulatory Framework

Every parameter in the Engine sheet carries an inline citation. Nothing is assumed without a regulatory basis.

| Regulation | What It Covers in This Model |
|---|---|
| **CRR Art. 92** | CET1, AT1, leverage ratio minimum requirements (Section 7) |
| **CRR Art. 428a–428at** | NSFR ASF/RSF factors by instrument and maturity (Section 6) |
| **CRR Art. 448** | Pillar 3 EVE disclosure — full cashflow discounting method (Section 14b) |
| **Del. Reg. (EU) 2022/786** | LCR outflow/inflow rates, HQLA haircuts by asset class (Section 5) |
| **EBA/GL/2022/14** | IRRBB shock scenarios, EVE outlier threshold, NII early warning, NMD behavioural caps (Sections 3, 4, 12, 14) |
| **EBA/GL/2024/35** | Maturity ladder methodology, liquidity survival horizon (Section 13) |

---

## What Makes This Model Different

Most student or portfolio Excel models pick one or two metrics and hardcode the rest. This model does not.

**Formula-only architecture.** No VBA, no macros. Every scenario output — across all 18 sections — is driven by a single `CHOOSE` call in the Engine that reads the Dashboard dropdown. Delete the scenario selector and the whole model breaks. That is the point: it is genuinely interconnected.

**Inline regulatory citations.** Every behavioural parameter, haircut, and threshold in the Engine sheet has its regulatory basis written next to it (EBA article, CRR article, Delegated Regulation article). This is how real models are documented for internal audit and regulatory review.

**Calibrated to real actuals.** The balance sheet is built from Q4 2025 Pillar 3 disclosures — the model checks against actual numbers, not invented ones. The 2025A NII cross-check is €0.

**Dual EVE methodology.** Both the simplified PVBP/duration-weighted method (EBA/GL/2022/14 Annex II) and the full cashflow discounting method (CRR Art. 448 Pillar 3) are implemented and compared — section 14 vs 14b.

---

## How to Use

1. Open `MAJOR_EUROPEAN_GSIB_ALM_Model_v10.xlsx` in Excel 2016 or later
2. Go to the **Dashboard** tab
3. Use the **▶ ACTIVE SCENARIO** dropdown (top right) to select: Base / Rate Hike / Rate Cut / Stress
4. All 18 sections update automatically — no manual steps needed
5. Navigate to the **Model** tab for section-level detail
6. Use the **Engine** tab to modify rate assumptions, spreads, or behavioural parameters

> **Important:** Yellow cells in the Engine are formula outputs — do not edit them. White/blue input cells are the only cells you should change.

---

## File Structure

```
excel-model/
├── MAJOR_EUROPEAN_GSIB_ALM_Model_v10.xlsx   ← Full working model
├── ALM_Master_Model_Showcase_v12.pdf        ← Full showcase (cover, summary, all sections)
├── README.md                                 ← This file
└── LICENSE.txt                               ← CC BY-NC 4.0
```

---

## Data Sources & Disclaimer

Balance sheet actuals calibrated to Q4 2025 public disclosures of a major European G-SIB (publicly available Pillar 3 report). No proprietary data used. All regulatory parameters reference publicly available EBA guidelines and EU regulations, cited inline throughout the model.

Built for portfolio and educational purposes only. Not intended as investment or regulatory advice.

---

## Part of the ALM Python Portfolio

This Excel model is the analytical foundation. The [ALM Python Portfolio](https://github.com/HossamEltarrass/ALM-Python-Portfolio) replicates every section of this model in Python — turning static calculations into automated, version-controlled, testable code.

| Project | Python Equivalent of |
|---|---|
| P1 — NII Scenario Tool | Sections 1, 2, 10 |
| P2 — IRRBB Stress Testing | Sections 3, 4 |
| P3 — LCR/NSFR Calculator | Sections 5, 6 |
| P4 — Bond Pricing & Duration | Section 14 |
| P5 — Yield Curve Bootstrap | YieldCurve sheet |
| P6 — FTP Framework | Engine (spread assumptions) |
| P7 — CPR Behavioural Model | Engine (Section A4) |
| P8 — ICAAP Stress Testing | Sections 7, 9, 10 |
| P9 — Hedge Effectiveness | Section 4 (hedged EVE) |
| P10 — Maturity Ladder | Section 13 |
| P11 — Capital Forecasting | Section 7 |
| P12 — ALM Dashboard | Dashboard |

---

## License

Licensed under [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

Free to use, share, and adapt for non-commercial purposes with attribution.

---

## Author

**Hossam Eltarrass**
ALM Intern | BSc Banking & Finance — University of Siena

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-darkgreen)](https://linkedin.com/in/hossameltarrass)
[![GitHub](https://img.shields.io/badge/GitHub-Portfolio-darkgreen)](https://github.com/HossamEltarrass)

---

*Model v10 · Calibrated to Q4 2025 Actuals · Last updated: May 2026 · All figures EUR millions*
