# Project 8 of 12 — ICAAP Stress Testing Framework
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview

This project implements a professional **ICAAP Severe Stress Testing Engine** in Python, calibrated to the full balance sheet of a major European G-SIB (anonymised). It is the eighth project in a Python ALM portfolio built to demonstrate junior analyst capability in asset-liability management.

The **ICAAP** (Internal Capital Adequacy Assessment Process) is the bank's own self-assessment — required under CRD V Art.73 and Basel III Pillar 2 — of whether it holds enough capital and liquidity to survive a **severe but plausible** stress scenario. The output feeds directly into the ECB's **SREP** (Supervisory Review and Evaluation Process).

What makes this project unique in the series is its scope: rather than stress-testing a single metric in isolation, the ICAAP engine simultaneously applies one unified severe shock across **all six regulatory metrics** — NII, Net Income, CET1, LCR, NSFR, and EVE — and produces a single **traffic light summary table** ready for ALCO presentation.

All figures are in **EUR millions (€m)**.

---

## 2. Regulatory Context

| Regulation | Requirement |
|---|---|
| **CRD V Art.73** | Banks must maintain an ICAAP covering all material risks |
| **Basel III Pillar 2** | Internal capital assessment submitted to supervisors (SREP) |
| **EBA/GL/2021/05** | ICAAP and ILAAP guidelines — scenario design and governance |
| **CRR Art.92** | CET1 minimum ratio: Pillar 1 + Pillar 2R + combined buffers |
| **Del. Reg. (EU) 2022/786** | LCR minimum: 100% |
| **CRR Art.428b (CRR2)** | NSFR minimum: 100% |
| **EBA/GL/2022/14 para 114** | EVE outlier test: > 15% of Tier 1 = outlier institution |

---

## 3. Severe Stress Scenario

The ICAAP severe scenario combines five simultaneous shocks — no single shock alone qualifies as ICAAP-grade stress:

| Parameter | Base 2026F | Severe Stress | Rationale |
|---|---|---|---|
| Rate Shock | 0 bps | **+300 bps** | ECB adverse macro scenario |
| Loan Growth | +3% | **−5%** | Credit contraction and demand collapse |
| Deposit Outflow | +2.5% | **−15%** | Behavioural stress and reputational shock |
| Cost of Risk | 25 bps | **100 bps** | NPL ratio surge in stress environment |
| Cost / Income | 62% | **70%** | Revenue compression + sticky cost base |

Source: `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` — Model Sheet, Section 17, rows D335:D339

---

## 4. Balance Sheet (2025A / 2026F)

### Assets

| Item | 2025A (€m) | 2026F (€m) | Severe (€m) |
|---|---|---|---|
| Cash & CB Reserves | 211,330 | 214,325 | 214,325 |
| Loans to Customers | 897,358 | 924,279 | **852,490** |
| Interbank Loans | 26,259 | 26,259 | 26,259 |
| Securities Portfolio | 153,107 | 157,700 | 157,700 |

### Liabilities

| Item | 2025A (€m) | 2026F (€m) | Severe (€m) |
|---|---|---|---|
| Customer Deposits | 1,075,564 | 1,102,453 | **914,229** |
| Interbank Funding | 69,938 | 69,938 | 69,938 |
| Repo Funding | 357,947 | 357,947 | 357,947 |
| Bonds Issued | 173,933 | 173,933 | 173,933 |
| Subordinated Debt | 34,468 | 34,468 | 34,468 |

**Tier 1 Capital (CET1 €109,924m + AT1 €22,249m): €132,173m**

---

## 5. Methodology

### NII (Net Interest Income)

The NII engine reprices every balance sheet item using the rate movement from 2025A to 2026F plus the +300bps shock, weighted by each item's repricing sensitivity. Volumes are adjusted for the loan contraction and deposit outflow.

```
Loan yield severe   = Loan yield 2025A + Loan beta × (Euribor 2026F + shock − Euribor 2025A)
Deposit rate severe = max(0, Dep rate 2025A + Dep beta × (ECB 2026F + shock − ECB 2025A))
NII severe          = Σ(Asset balance × stressed rate) − Σ(Liability balance × stressed rate)
```

Stressed volumes: Loans = 2025A × 0.95 | Deposits = 2025A × 0.85

### Net Income

```
Revenue      = NII severe + Fee income (0.8% × total assets, unchanged)
Pre-tax      = Revenue × (1 − CIR 70%) − CoR 100bps × stressed loan balance
Net Income   = Pre-tax × (1 − 25% tax)
```

### CET1 Ratio

```
Equity severe = Equity 2025A + Net Income severe × (1 − 60% payout)
RWA severe    = Loans × 75% + Securities × 20% + IB Loans × 20% + Trading × 15%
CET1 severe   = Equity severe / RWA severe
```

Loan contraction (−5%) shrinks RWA significantly — CET1 improves under this stress.

### LCR

```
Deposit outflow ICAAP = 2025A deposits × 15% (flat run-off, replaces tiered LCR rates)
Non-deposit outflows  = Base 2026F outflows − base deposit runoff buckets
Stressed net outflows = Deposit outflow + Non-deposit outflows − min(Inflows, 75% cap)
LCR severe            = HQLA 2026F / stressed net outflows
```

### NSFR

```
ASF reduction = 2025A deposits × 15% × (70% stable × 90% ASF + 30% less-stable × 80% ASF)
ASF severe    = ASF 2026F − ASF reduction
NSFR severe   = ASF severe / RSF 2026F   (RSF unchanged — structural mismatch persists)
```

### EVE / Tier 1

```
Net EVE loss   = |PVBP × 300bps × (1 − 55% hedge ratio)|
EVE / T1 ratio = Net EVE loss / Tier 1 capital 2025A
```

---

## 6. Key Results

### ICAAP Stress Summary Table

| Metric | Reg. Minimum | Base 2026F | Severe Stress | Change | Traffic Light |
|---|---|---|---|---|---|
| NII (€m) | EWI: >−10% | 22,686 | **15,355** | −7,331 | RED |
| Net Income (€m) | > 0 | 11,194 | **2,162** | −9,032 | GREEN |
| CET1 Ratio | ≥ 13.5% | 15.88% | **16.49%** | +0.61pp | GREEN |
| LCR | ≥ 100% | 153.55% | **111.52%** | −42.0pp | GREEN |
| NSFR | ≥ 100% | 96.02% | **85.83%** | −10.2pp | RED |
| EVE / Tier 1 | < 15% | 13.24% | **19.87%** | +6.62pp | RED |

**Result: 3 RED — MANAGEMENT ACTION REQUIRED**

---

## 7. Key Insights

**1. CET1 Paradox — Capital Improves Under Severe Stress**
The CET1 ratio rises from 15.88% to 16.49% under the severe scenario. This counterintuitive result occurs because the +300bps rate shock still generates positive Net Income (€2.2bn), adding retained earnings, while the loan contraction (−5%) shrinks RWA by more than equity declines. This is a core ALM insight: short-run capital ratios can improve even as long-run economic value (EVE) deteriorates sharply.

**2. NII vs EVE — The Fundamental ALM Tension**
NII under stress: +€15.4bn (positive income). EVE under stress: −€26.3bn loss (19.87% of Tier 1, breaching the 15% outlier threshold). The +300bps shock benefits the next 12 months of floating-rate income but destroys the long-duration economic value of the banking book. The bank earns more in the short run and is worth less in the long run.

**3. NSFR — The Structural Vulnerability**
NSFR was already below 100% in the base 2026F (96.02%) due to the insurance asset book (€311.6bn at 100% RSF with no matching ASF). The 15% deposit outflow removes a further €140bn of stable funding, pushing NSFR to 85.83%. No amount of short-term liquidity management fixes a structural RSF mismatch of this scale.

**4. LCR Resilience**
Despite a 15% deposit run, LCR holds at 111.52% because the HQLA buffer (€365.4bn) is large enough to absorb the shock. Short-term liquidity is not the bank's weakness; structural liquidity (NSFR) is.

**5. EVE Outlier — Hedge Effectiveness Tested**
The 55% IRS hedge overlay reduces the gross EVE exposure (€58.4bn) to a net EVE loss of €26.3bn. But at +300bps — a more extreme shock than the standard EBA +200bps — even the hedged position breaches the 15% Tier 1 outlier threshold.

---

## 8. Management Actions Required

| Issue | Action |
|---|---|
| NSFR Breach (85.83%) | Issue ≥1Y senior unsecured bonds or attract term deposits to rebuild ASF |
| EVE Outlier (19.87%) | Increase IRS hedge ratio above 55% or shorten asset duration via portfolio management |
| NII EWI Triggered | Monitor deposit repricing pass-through; consider rate floor strategy |
| Capital headroom | CET1 buffer (16.49% vs 13.5% min) = 2.99pp headroom — no immediate capital action needed |

---

## 9. How Each Prior Project Feeds Into ICAAP

| Source Project | What It Contributes |
|---|---|
| **Project 1 — NII Tool** | NII formula structure and repricing beta framework |
| **Project 2 — IRRBB** | PVBP and EVE calculation methodology |
| **Project 3 — LCR/NSFR** | HQLA, outflow rates, ASF/RSF factors |
| **Project 4 — Bond Pricing** | DV01 / duration concepts underpinning PVBP |
| **Project 5 — Yield Curve** | 2026F market rate forecast (ECB, Euribor, swap) |
| **Project 6 — FTP** | Cost of funds framework informing repricing spreads |
| **Project 7 — CPR** | 2026F balance sheet volumes and Tier 1 capital proxy |

The ICAAP is the synthesis of all prior ALM projects — all metrics in one unified stress table.

---

## 10. Limitations

- Static balance sheet — no modelling of new business inflows replacing runoff
- Simplified RWA — uses fixed risk weights per asset class, not full SA/IRB calculation
- No second-round effects — credit losses do not feed back into deposit outflows
- Flat deposit outflow — does not distinguish by depositor type (retail vs wholesale)
- NSFR RSF unchanged — does not model asset fire-sales or HQLA drawdown effect on RSF
- Tax treatment simplified — does not model deferred tax assets on stressed losses

---

## 11. ALM Takeaway

The ICAAP reveals a three-way stress convergence: income collapses by 32.3%, structural funding breaches the NSFR minimum, and EVE sensitivity breaches the outlier threshold simultaneously — exactly the correlated shock scenario that makes severe stress genuinely dangerous. The CET1 ratio paradoxically improves to 16.49% because the contracting loan book shrinks RWAs faster than it erodes capital, a common ICAAP artefact that the ECB explicitly scrutinises to ensure banks are not disguising weakness behind ratio improvements. In practice, the RED flags on NII, NSFR, and EVE would trigger mandatory management actions — dividend suspension, accelerated MREL issuance, and IRS overlay expansion — each of which the bank must demonstrate to the supervisor as credible, costed, and executable within the recovery timeline.

---

## 12. Cross-Check vs Excel Section 17

| Metric | Excel (§17) | Python | Difference | Status |
|---|---|---|---|---|
| NII (€m) | 15,354.6 | 15,355 | < 5 | ✅ |
| Net Income (€m) | 2,162.0 | 2,162 | 0.0 | ✅ |
| CET1 Ratio | 16.49% | 16.49% | 0.00pp | ✅ |
| LCR | 111.52% | 111.52% | 0.00pp | ✅ |
| NSFR | 85.83% | 85.83% | 0.00pp | ✅ |
| EVE / Tier 1 | 19.87% | 19.87% | 0.00pp | ✅ |

All six metrics match Excel Section 17 within rounding tolerance. ✅

---

## 13. Files

| File | Description |
|---|---|
| `ICAAP_Stress_Testing.ipynb` | Main notebook (9 cells) |
| `ICAAP_Stress_Testing_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source Excel model (Section 17) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
*Methodology: CRD V Art.73 | Basel III Pillar 2 | EBA/GL/2021/05 | EBA/GL/2022/14*
---
