# Project 1 of 12 — NII Scenario Tool
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview
This tool simulates how a major European G-SIB's Net Interest Income (NII) changes under four interest rate scenarios using a static 2025A balance sheet. It applies rate shocks to each balance sheet item according to its repricing behaviour — distinguishing between fully floating, partially floating, and fixed-rate instruments. The output is a scenario comparison table and professional chart showing NII sensitivity, one of the core outputs reviewed by a bank's ALCO on a monthly basis.

## 2. Regulatory Context
Scenarios are calibrated to the Bank's ALM Engine assumptions and aligned with **EBA/GL/2022/14** IRRBB regulatory guidance. The deposit beta assumptions vary by scenario (0.40 Base → 0.60 Stress), reflecting the partial pass-through of rate moves to depositors and the competitive dynamics of each rate environment.

## 3. Balance Sheet Summary

All figures in EUR millions. Reference year: 2025A.

**Assets**

| Item | Balance (€m) | Base Rate | Repricing Factor |
|---|---|---|---|
| Cash & CB reserves | 211,330 | 2.50% | 1.0 × shock |
| Loans to customers | 897,358 | 3.80% | 0.9 × shock (loan beta) |
| Interbank loans | 26,259 | 3.10% | 1.0 × shock |
| Securities portfolio | 153,107 | 3.00% | 0.0 × shock (fixed) |

**Liabilities**

| Item | Balance (€m) | Base Rate | Repricing |
|---|---|---|---|
| Customer deposits | 1,075,564 | 0.50% | Deposit beta × shock |
| Interbank funding | 69,938 | 3.10% | 1.0 × shock |
| Repo funding | 357,947 | 2.415% | 1.0 × shock |
| Bonds issued | 173,933 | 3.25% | 0.0 × shock (fixed) |
| Subordinated debt | 34,468 | 2.50% | 0.0 × shock (fixed) |

## 4. Methodology

Each balance sheet item is assigned a repricing factor determining how much of a rate shock it absorbs. Customer deposit rates do not reprice dollar-for-dollar with market rates — the deposit beta captures the partial pass-through:

```
New deposit rate = Base deposit rate + (rate shock x deposit beta)
```

NII is then computed as:

```
Interest Income  = Sum (balance x new rate) for each asset
Interest Expense = Sum (balance x new rate) for each liability
NII              = Interest Income - Interest Expense
```

**Scenarios (EBA/GL/2022/14 alignment):**

| # | Name | Rate Shock | Deposit Beta | Rationale |
|---|---|---|---|---|
| 1 | Base | 0 bp | 0.40 | Current ECB environment (2.50% DFR) |
| 2 | Rate Hike | +200 bp | 0.50 | Inflation resurgence / ECB tightening |
| 3 | Rate Cut | -200 bp | 0.30 | Recession / ECB easing cycle |
| 4 | Stress | +300 bp | 0.60 | Severe inflation shock |

## 5. Key Results

| Scenario | Rate Shock | NII (€m) | Change vs Base |
|---|---|---|---|
| Base | 0 bp | 22,085 | — |
| Rate Hike | +200 bp | 23,676 | +1,591 |
| Rate Cut | -200 bp | 16,192 | -5,893 |
| Stress | +300 bp | 21,245 | -840 |

The bank is asset-sensitive at +200bp, generating an additional €1,591m of NII. However, the institution becomes liability-sensitive under extreme stress (+300bp), where the large repo book and higher deposit beta push liability costs above asset income gains. The largest downside risk is a falling rate environment: a -200bp cut reduces NII by €5,893m — approximately 27% of the base.

## 6. Cross-Check vs Excel

| Metric | Excel 2025A | Python 2025A | Difference |
|---|---|---|---|
| Base NII (€m) | 22,085.3 | 22,085.3 | 0.0 ✅ |

Python replicates the Excel master model exactly (difference = €0).

## 7. ALM Takeaway

The bank's NII profile is asset-sensitive: a +200bps parallel shift adds €1,591m to annual income, while a -200bps cut removes €5,893m — an asymmetric exposure reflecting the repricing advantage of floating-rate assets offset by fixed-rate liabilities. As the ECB moves toward rate cuts in 2025-2026, this sensitivity positions the bank to lose income unless Treasury actively reduces the asset-sensitivity gap through fixed-rate lending or pay-fixed IRS overlays.

## 8. Files

| File | Description |
|---|---|
| `NII_Scenario_Tool.ipynb` | Main notebook |
| `NII_Scenario_Tool_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source balance sheet data — Major European G-SIB ALM Model (2025A) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
---
