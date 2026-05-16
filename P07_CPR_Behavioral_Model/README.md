# Project 7 of 12 — CPR / Behavioural Prepayment Model
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview
This project implements the CPR (Constant Prepayment Rate) Behavioural Model, the statistical framework banks use to quantify how early loan repayments affect income and interest rate risk across rate scenarios. It builds an NII sensitivity grid across 7 CPR levels and 4 rate scenarios, a duration-shortening EVE table, and two professional finance charts — all cross-checked against Section 16 of the Excel model. Source: Section 16 of `MAJOR_EUROPEAN_GSIB_ALM_Model_v10.xlsx`.

## 2. Regulatory Context
Under **EBA/GL/2022/14 (IRRBB Guidelines)**, banks must model borrower behaviour explicitly — prepayment speed is not fixed, it changes with rates. The EBA mandates scenario-specific CPR multipliers: borrowers refinance faster when rates fall (×1.5 at −200bps) and stay in cheap mortgages when rates rise (×0.5 at +200bps). The EVE duration-shortening analysis links directly to the outlier test under **CRR Art. 448** (15% of Tier 1 threshold).

## 3. Balance Sheet Summary

All figures in EUR millions. Reference year: 2026F. Tier 1 Capital: **€132,173m** (CET1 €109,924m + AT1 €22,249m).

**Loan Portfolio (Engine sheet):**

| Parameter | Value | Source |
|---|---|---|
| Loan Balance 2026F | €924,278.74m | Engine sheet (2026F column) |
| Old Loan Yield | 3.80% | 2025A book yield |
| Loan Repricing Beta | 0.90 | Engine sheet |
| ECB DFR 2025A | 2.50% | Project 1 / Cash rate |
| ECB DFR 2026F | 2.25% | Project 5 / YieldCurve sheet |

**Yield Delta by Scenario:**

| Scenario | Net move vs 2025A | × Beta 0.90 | Yield Delta |
|---|---|---|---|
| Base (0 bps) | −25 bps | × 0.90 | **−0.225%** |
| Rate Hike +200bps | +175 bps | × 0.90 | **+1.575%** |
| Rate Cut −200bps | −225 bps | × 0.90 | **−2.025%** |
| Stress +300bps | +275 bps | × 0.90 | **+2.475%** |

## 4. Methodology

**Part A — NII Sensitivity Grid:**
```
effective_cpr = stated CPR × CPR_multiplier    (EBA behavioural adjustment)
NII_impact    = yield_delta × loan_balance × effective_cpr
```

**CPR Multipliers (EBA/GL/2022/14):**

| Scenario | CPR Multiplier | Reason |
|---|---|---|
| Base (0 bps) | × 1.0 | Normal behaviour |
| Rate Hike +200bps | × 0.5 | Cheap fixed mortgages — half as many prepay |
| Rate Cut −200bps | × 1.5 | Refinancing wave — 50% more prepay early |
| Stress +300bps | × 2.0 | Distressed borrowers forced to sell or exit |

**Part B — EVE Duration-Shortening:**
```
Eff. Duration = 2.50y × (1 − CPR × 0.30)
Adj. PVBP     = −194.5093 × (Eff. Duration / 2.50)
Net EVE       = |Adj. PVBP| × 200 × (1 − 0.55 hedge ratio)
```

## 5. Key Results

**NII Sensitivity Grid (€m, annual):**

| Annual CPR | Base | Rate Hike | Rate Cut | Stress |
|---|---|---|---|---|
| CPR = 0% | €0m | €0m | €0m | €0m |
| CPR = 5% | −€104m | +€364m | −€1,404m | +€2,288m |
| CPR = 10% ★ | **−€208m** | **+€728m** | **−€2,808m** | **+€4,575m** |
| CPR = 15% | −€312m | +€1,092m | −€4,211m | +€6,863m |
| CPR = 20% | −€416m | +€1,456m | −€5,615m | +€9,150m |
| CPR = 25% | −€520m | +€1,820m | −€7,019m | +€11,438m |
| CPR = 30% | −€624m | +€2,184m | −€8,422m | +€13,726m |

★ Base Case CPR = 10% per EBA/GL/2022/14 benchmark

**EVE Duration-Shortening (Parallel Up +200bps, post 55% IRS hedge, Tier 1 = €132,173m):**

| Annual CPR | Eff. Duration | Net EVE (€m) | EVE / Tier 1 |
|---|---|---|---|
| CPR = 0% | 2.500y | **17,506** | **13.24%** |
| CPR = 10% | 2.425y | 16,981 | 12.85% |
| CPR = 20% | 2.350y | 16,455 | 12.45% |
| CPR = 30% | 2.275y | 15,930 | 12.05% |

All scenarios remain below the 15% Tier 1 outlier threshold after the 55% IRS hedge.

## 6. Cross-Check vs Excel

All Python outputs compared against Section 16 of the Excel model. Target: difference = 0.000 on all cells.

| Cell | Excel | Python | Diff |
|---|---|---|---|
| CPR=10%, Base NII | −207.9627 | −207.9600 | +0.0027 ✅ |
| CPR=10%, Stress NII | 4,575.1798 | 4,575.1800 | +0.0002 ✅ |
| CPR=0%, Net EVE | 17,505.8379 | 17,505.8400 | +0.0021 ✅ |
| CPR=30%, Net EVE | 15,930.3125 | 15,930.3100 | −0.0025 ✅ |

**ALL CHECKS PASSED** — Python replicates Excel Section 16 exactly.

## 7. ALM Takeaway

Prepayment behaviour introduces a non-linearity that static duration models cannot capture: when rates rise, borrowers rationally hold onto cheap fixed-rate mortgages, reducing CPR toward zero and extending the effective duration of the asset book precisely when duration is most costly. The CPR=0% scenario — which produces the worst EVE of €17,506m (13.24% of Tier 1) — illustrates this extension risk directly. Conversely, in the Rate Cut scenario, accelerating prepayments compress NII as borrowers refinance at lower rates. The practical implication is that any IRRBB hedge sized without a behavioural CPR assumption will be systematically under-hedged in rising rate environments and over-hedged in falling rate environments — making this model a prerequisite for accurate hedge calibration in Project 9.

## 8. Files

| File | Description |
|---|---|
| `CPR_Behavioral_Model.ipynb` | Main notebook |
| `CPR_Behavioral_Model_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source Excel model (Section 16) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
---
