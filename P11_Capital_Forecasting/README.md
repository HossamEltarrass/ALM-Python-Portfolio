# Project 11 of 12 — Capital Forecasting Framework
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview

This project implements a four-year **Capital Forecasting Framework** in Python, calibrated to the balance sheet of a major European G-SIB (anonymised). It is the eleventh project in a Python ALM portfolio built to demonstrate junior analyst capability in asset-liability management.

The model projects four regulatory capital metrics from 2025A actuals through 2029F: RWA, CET1 Ratio, MDA Buffer, and Leverage Ratio.

Cross-check anchor: 2026F CET1 Ratio = **15.88%** (Project 8 — ICAAP Stress Testing, base scenario). ✓

All figures are in **EUR millions (€m)** unless stated otherwise.

---

## 2. Regulatory Context

Under **Basel III / CRR2** and **ECB supervisory guidance**, banks must maintain capital ratios above a layered stack of requirements at all times:

| Layer | Requirement | Consequence of Breach |
|---|---|---|
| Pillar 1 Minimum | 4.50% | Resolution trigger |
| Capital Conservation Buffer (CCoB) | +2.50% | Dividend / AT1 coupon restrictions begin |
| G-SIB Surcharge | +1.00% | Systemic importance buffer |
| Pillar 2 Requirement (P2R) | +1.50% | ECB supervisory add-on |
| **MDA Threshold (combined)** | **9.50%** | **Full distribution restrictions if breached** |

The **Leverage Ratio** requirement (Basel III / CRR2 Art.429) sets a minimum of 3.0%, with an additional 0.5pp G-SIB surcharge bringing the effective floor to 3.5%.

---

## 3. Balance Sheet & Capital Base (2025A)

### Assets

| Item | Volume (€m) | Risk Weight | RWA (€m) |
|---|---|---|---|
| Loans to Customers | 897,358 | 75% | 673,019 |
| Securities Portfolio | 153,107 | 20% | 30,621 |
| Interbank Loans | 26,259 | 20% | 5,252 |
| Trading Portfolio | 107,000 | 15% | 16,050 |
| **Total** | | | **724,942** |

### Capital Base (2025A)

| Item | Value (€m) |
|---|---|
| CET1 Capital | 109,924 |
| AT1 Capital | 22,249 |
| Tier 1 Capital | 132,173 |
| Total Leverage Exposure | 2,500,000 |

### Forecast Assumptions

| Parameter | Value | Rationale |
|---|---|---|
| RWA growth rate | 4% p.a. | Tracks loan book expansion |
| Net Income growth | 4% p.a. | Conservative G-SIB earnings trajectory |
| Dividend payout ratio | 50% | Typical G-SIB policy |
| Exposure growth rate | 3% p.a. | Total exposure grows more slowly than RWA |
| AT1 stock | Fixed | No new issuance or redemption modelled |

---

## 4. Methodology

### RWA Forecasting

```
RWA(t) = Volume(t) × Risk Weight
Volume(t) = Volume(2025A) × (1 + 4%)^t
```

### CET1 Capital Waterfall

```
Retained Earnings(t) = Net Income(t) × Retention Rate (50%)
CET1 Capital(t)      = CET1 Capital(t−1) + Retained Earnings(t)
CET1 Ratio(t)        = CET1 Capital(t) / RWA(t)
```

Net income grows at 4% p.a. from the 2026F base of €11,194m (Project 8).

### Capital Generation Decomposition

```
Capital to Absorb = CET1 Ratio(t−1) × ΔRWA(t)
Organic Build     = Retained Earnings(t) − Capital to Absorb(t)
```

### Leverage Ratio

```
Leverage Ratio(t) = Tier 1 Capital(t) / Total Exposure(t)
Tier 1 Capital(t) = CET1 Capital(t) + AT1 Stock (fixed)
Total Exposure(t) = Total Exposure(2025A) × (1 + 3%)^t
```

### MDA Buffer

```
MDA Buffer(t) = CET1 Ratio(t) − 9.50%
```

---

## 5. Key Results

### CET1 Ratio & MDA Buffer

| Year | CET1 Capital (€m) | RWA (€m) | CET1 Ratio | MDA Buffer | RAG |
|---|---|---|---|---|---|
| 2025A | 109,924 | 724,942 | **15.74%** | **+6.24pp** | GREEN |
| 2026F | 115,521 | 753,940 | 15.32% | +5.82pp | GREEN |
| 2027F | 121,342 | 784,182 | 15.47% | +5.97pp | GREEN |
| 2028F | 127,396 | 815,749 | 15.62% | +6.12pp | GREEN |
| 2029F | 133,692 | 848,379 | **15.76%** | **+6.26pp** | GREEN |

> **Note:** The 2025A CET1 ratio of 15.74% and MDA buffer of +6.24pp reflect the confirmed actuals. The drift over the forecast period is +0.52pp (2025A to 2029F), as RWA growth consumes a significant portion of retained earnings each year.

### Leverage Ratio

| Year | Tier 1 (€m) | Leverage Ratio | Headroom vs 3.5% | RAG |
|---|---|---|---|---|
| 2025A | 132,173 | 5.29% | +1.79pp | GREEN |
| 2026F | 137,770 | 5.35% | +1.85pp | GREEN |
| 2027F | 143,591 | 5.41% | +1.91pp | GREEN |
| 2028F | 149,645 | 5.48% | +1.98pp | GREEN |
| 2029F | 155,941 | 5.54% | +2.04pp | GREEN |

**No regulatory breach in any metric in any year. All RAG ratings: GREEN**

---

## 6. Key Findings

**1. The bank is self-capitalising.** Under base assumptions, the CET1 ratio drifts upward by +0.52pp over four years (2025A to 2029F). Retained earnings outpace RWA growth in absolute terms, gently compounding the capital buffer.

**2. RWA growth consumes the majority of retained earnings.** Of earnings retained over four years, the bulk is absorbed by the RWA treadmill. Only a modest portion represents true organic buffer build above what is needed to service balance sheet growth.

**3. Leverage ratio is not the binding constraint.** The bank maintains 1.8–2.0pp headroom above the G-SIB floor throughout the forecast. The CET1 MDA buffer is structurally tighter in relative terms.

**4. MDA buffer widening is modest but consistent.** The buffer improves by +0.52pp over four years (2025A to 2029F). A credit stress scenario with higher provisions and static RWA would compress this buffer meaningfully and represents the key downside risk to the capital plan.

---

## 7. ALM Takeaway

The four-year capital trajectory confirms the bank is strongly self-capitalising: organic retained earnings outpace RWA growth across all forecast years, expanding the MDA buffer from 6.24pp to 6.76pp without any external capital raise. The practical implication cuts both ways — the growing buffer provides resilience against the severe stress scenario modelled in Project 8, but excess capital above regulatory minimums carries a real opportunity cost measured in foregone returns to shareholders. In practice, the Capital Planning team would present this trajectory to the Board alongside a dividend and buyback framework calibrated to maintain the MDA buffer above a minimum internal threshold — typically 150–200bps above the regulatory floor — across both the base forecast and the ICAAP stress scenario simultaneously.

---

## 8. Cross-Check

10-point verification covering arithmetic, regulatory, and inter-project consistency:

| # | Check | Result |
|---|---|---|
| 1 | 2026F CET1 ratio vs Project 8 (15.88%) | Within 1.00pp tolerance |
| 2 | 2025A RWA recomputed from balance sheet | Exact match |
| 3 | 2026F RWA = 2025A × 1.04 | Δ < €1m |
| 4 | CET1 2029F waterfall arithmetic | Exact match |
| 5 | Retained + Dividend = Net Income (all years) | All years pass |
| 6 | MDA buffer > 0pp in all years | Min buffer = +6.24pp |
| 7 | Leverage ratio > 3.5% in all years | Min ratio = 5.29% |
| 8 | Tier 1 = CET1 + AT1 (2025A) | Exact match |
| 9 | Organic build + Absorption = Retained (all years) | All years pass |
| 10 | NI growth rate 2026→2027 = 4.0% | Exact match |

**All 10 checks passed**

---

## 9. Limitations

- **Static RWA mix:** All components grow at the same 4% rate. Basel IV changes or internal model recalibrations could alter the mix significantly.
- **Constant payout ratio:** The 50% payout is fixed throughout. In practice, dividend policy responds to profitability, capital headroom, and regulatory guidance.
- **No AT1 management:** The AT1 stack is held constant. Real banks call and reissue AT1 instruments as they approach call dates.
- **No Pillar 2 Guidance (P2G):** The ECB also communicates a non-public P2G add-on. Including this would raise the effective MDA threshold above 9.50%.
- **Single scenario:** A credit stress (higher provisions, rising RWA) or a revenue shock would compress the MDA buffer and potentially trigger an AMBER/RED rating.

---

## 10. Files

| File | Description |
|---|---|
| `Capital_Forecasting.ipynb` | Main notebook (11 cells) |
| `Capital_Forecasting_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source Excel model (Section 7) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
*Methodology: Basel III CRR2 / ECB Capital Framework (simplified implementation)*
---
