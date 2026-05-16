# ALM Python Portfolio
### Major European G-SIB | 2025A / 2026F | Hossam Eltarrass

A 12-project Python portfolio replicating the core outputs of an Asset-Liability Management (ALM) desk at a major European G-SIB. Each project is built from scratch in Python and cross-validated against a manually built Excel master model.

---

## Portfolio Structure

| # | Project | Topic | Key Output |
|---|---------|-------|------------|
| 00 | [ALM Excel Model](./00_ALM_Excel_Model/) | Master Excel Model | Multi-section ALM workbook *(coming soon)* |
| 01 | [NII Scenario Tool](./01_NII_Scenario_Tool/) | Net Interest Income | Base NII €22,085m — 4 rate scenarios |
| 02 | [IRRBB Stress Testing](./02_IRRBB_Stress_Testing/) | Interest Rate Risk | All 6 Basel scenarios — outlier institution |
| 03 | [LCR / NSFR Calculator](./03_LCR_NSFR_Calculator/) | Liquidity Risk | Stress NSFR breach at 99.8% |
| 04 | [Bond Pricing & Duration](./04_Bond_Pricing_Duration/) | Market Risk | Portfolio DV01 €100.88m/bp |
| 05 | [Yield Curve Bootstrap](./05_Yield_Curve_Bootstrap/) | Rates | EUR zero curve — 10Y annual |
| 06 | [FTP Framework](./06_FTP_Framework/) | Funds Transfer Pricing | Total FTP NII €23,975m |
| 07 | [CPR Behavioural Model](./07_CPR_Behavioural_Model/) | Prepayment | NII sensitivity grid 7×4 scenarios |
| 08 | [ICAAP Stress Testing](./08_ICAAP_Stress_Testing/) | Capital & Liquidity | 3 RED metrics — management action required |
| 09 | [Hedge Effectiveness](./09_Hedge_Effectiveness/) | IRS Overlay | All 6 Basel scenarios within 15% T1 limit |
| 10 | [Monthly NII & Maturity Ladder](./10_Monthly_NII_Maturity_Ladder/) | Liquidity Horizon | Base 9M / Stress 2M survival horizon |
| 11 | [Capital Forecasting](./11_Capital_Forecasting/) | Capital Planning | CET1 15.16%→15.76% over 4 years |
| 12 | [ALM Dashboard Capstone](./12_ALM_Dashboard_Capstone/) | ALCO MIS Pack | 6-sheet Excel dashboard — RAG 7G/2A/4R |

---

## Regulatory Frameworks Covered

EBA/GL/2022/14 (IRRBB) · BCBS 368 · Basel III CRR2 · CRD V Art.73 · Del. Reg. (EU) 2022/786 (LCR) · CRR Art.428 (NSFR) · EBA/GL/2021/05 (ICAAP/ILAAP)

## Tech Stack

Python · pandas · numpy · matplotlib · scipy · xlwings · Jupyter

---

*Institution: Major European G-SIB (anonymised) | Reference years: 2025A actuals / 2026F forecast | Author: Hossam Eltarrass*
