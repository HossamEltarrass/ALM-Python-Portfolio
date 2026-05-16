# Project 2 of 12 — IRRBB Stress Testing Framework
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview
This project implements a professional Interest Rate Risk in the Banking Book (IRRBB) Stress Testing Framework in Python, calibrated to the balance sheet of a major European G-SIB. It computes ΔEVE and ΔNII across all six Basel standard shock scenarios, runs the supervisory outlier test, and cross-validates results against an Excel master model. This is the second project in a Python ALM portfolio built to demonstrate junior analyst capability in asset-liability management.

## 2. Regulatory Context
Under **Basel BCBS 368 (2016)** and **EBA IRRBB Guidelines**, banks are required to:

1. Apply six standardised interest rate shock scenarios to their banking book
2. Report the impact on **Economic Value of Equity (ΔEVE)** and **Net Interest Income (ΔNII)**
3. Submit to a **supervisory outlier test**: if |ΔEVE| > 15% of Tier 1 capital under any scenario, the bank is classified as an **outlier institution** — a regulatory red flag requiring management action

## 3. Balance Sheet Summary

All figures in EUR millions. Reference year: 2025A.

> **Note on Tier 1 Capital:** The notebook uses a simplified proxy of €80,000m for Tier 1 in its internal calculations. The actual confirmed Tier 1 Capital for this G-SIB is **€132,173m** (CET1 €109,924m + AT1 €22,249m), as used in Projects 7, 8, 9, and 11. The outlier percentages below reflect the actual Tier 1 figure.

**Assets**

| Item | Volume (€m) | Rate | Mod. Duration |
|---|---|---|---|
| Cash & CB Reserves | 211,330 | 2.50% | 0.25 yrs |
| Loans to Customers | 897,358 | 3.80% | 2.00 yrs |
| Interbank Loans | 26,259 | 3.10% | 0.25 yrs |
| Securities Portfolio | 153,107 | 3.00% | 4.50 yrs |

**Liabilities**

| Item | Volume (€m) | Rate | Mod. Duration |
|---|---|---|---|
| Customer Deposits | 1,075,564 | 0.50% | 0.50 yrs |
| Interbank Funding | 69,938 | 3.10% | 0.25 yrs |
| Repo Funding | 357,947 | 2.415% | 0.25 yrs |
| Bonds Issued | 173,933 | 3.25% | 3.50 yrs |
| Subordinated Debt | 34,468 | 2.50% | 5.00 yrs |

## 4. Methodology

**EVE Calculation:**

```
ΔPV(item) = −Modified Duration × Rate Shock × Volume
ΔEVE = Σ ΔPV(assets) − Σ ΔPV(liabilities)
```

Each item is assigned to a duration bucket: short (mod_duration ≤ 1 year) receives the short-rate shock; long (mod_duration > 1 year) receives the long-rate shock.

**NII Calculation:**

```
ΔIncome(asset)  = Volume × Repricing Factor × Short Shock
ΔCost(deposit)  = Volume × Deposit Beta    × Short Shock
ΔCost(other)    = Volume × Repricing Factor × Short Shock
ΔNII = Σ ΔIncome(assets) − Σ ΔCost(liabilities)
```

**Six Basel Standard Shock Scenarios:**

| # | Scenario | Short Rates | Long Rates |
|---|---|---|---|
| 1 | Parallel Up | +200bp | +200bp |
| 2 | Parallel Down | −200bp | −200bp |
| 3 | Steepener | −100bp | +100bp |
| 4 | Flattener | +100bp | −100bp |
| 5 | Short Rate Up | +250bp | 0bp |
| 6 | Short Rate Down | −250bp | 0bp |

## 5. Key Results

**Base NII: €22,085m** — consistent with Project 1. The institution is structurally asset-sensitive: asset duration exceeds liability duration.

**ΔEVE Results (Tier 1 Capital: €132,173m):**

| Scenario | ΔEVE (€m) | % of Tier 1 | Outlier? |
|---|---|---|---|
| Parallel Up | −22,345 | 16.9% | ⚠️ YES |
| Parallel Down | +22,345 | 16.9% | ⚠️ YES |
| Steepener | −22,879 | 17.3% | ⚠️ YES — Worst |
| Flattener | +22,879 | 17.3% | ⚠️ YES |
| Short Rate Up | −14,634 | 11.1% | ⚠️ YES |
| Short Rate Down | +14,634 | 11.1% | ⚠️ YES |

**Result: OUTLIER INSTITUTION — all 6 scenarios breach the 15% Tier 1 threshold.**

The steepener is the worst scenario for EVE: long rates rise (+100bp) while short rates fall (−100bp), causing large PV losses on long-duration assets. The fundamental ALM tension is clear — rising rates boost NII (+€3,742m under Parallel Up) while destroying EVE (−€22,345m, worst at Parallel Up = 16.9% of Tier 1).

## 6. Cross-Check vs Excel

Manual item-by-item ΔEVE computation under Parallel Up (+200bp):

| Item | Duration | Volume (€m) | ΔPV (€m) |
|---|---|---|---|
| Cash & CB Reserves | 0.25 | 211,330 | −1,056.7 |
| Loans to Customers | 2.00 | 897,358 | −35,894.3 |
| Interbank Loans | 0.25 | 26,259 | −131.3 |
| Securities Portfolio | 4.50 | 153,107 | −13,779.6 |
| **Total ΔPV Assets** | | | **−50,861.9** |
| Customer Deposits | 0.50 | 1,075,564 | −10,755.6 |
| Interbank Funding | 0.25 | 69,938 | −349.7 |
| Repo Funding | 0.25 | 357,947 | −1,789.7 |
| Bonds Issued | 3.50 | 173,933 | −12,175.3 |
| Subordinated Debt | 5.00 | 34,468 | −3,446.8 |
| **Total ΔPV Liabilities** | | | **−28,517.2** |
| **Manual ΔEVE** | | | **−22,344.7** |
| **Engine ΔEVE** | | | **−22,345.0** |
| **Difference** | | | **€0.3m (rounding)** |

✅ Cross-check passed

## 7. ALM Takeaway

The bank is classified as an outlier institution under EBA/GL/2022/14, with EVE sensitivity breaching the 15% Tier 1 threshold across all six Basel scenarios. The worst case — Parallel Up at 16.9% of Tier 1 — reflects the same asset-sensitive duration gap that boosts NII in rising rate environments: the bank benefits on income but suffers on economic value. Resolving this outlier status requires the Treasury desk to reduce the duration gap, typically through receive-fixed IRS overlays or shortening the maturity of fixed-rate assets — both of which carry an NII cost that must be weighed against the regulatory capital exposure.

## 8. Files

| File | Description |
|---|---|
| `IRRBB_Stress_Testing.ipynb` | Main notebook |
| `IRRBB_Stress_Testing_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source balance sheet data — Major European G-SIB ALM Model (2025A) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
---
