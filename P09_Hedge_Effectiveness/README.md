# Project 9 of 12 — Hedge Effectiveness: IRS Overlay
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview

This project implements a professional **Hedge Effectiveness Summary** in Python, replicating Section 18 of the Major European G-SIB ALM Model (anonymised). It decomposes the bank's EVE exposure into three components — Gross EVE, IRS Hedge Offset, and Net EVE — across all six Basel IRRBB standard shock scenarios, and confirms the bank remains within the regulatory outlier threshold post-hedge.

All figures are in **EUR millions (€m)**.

---

## 2. Regulatory Context

Under **EBA/GL/2022/14 Annex I** and **CRR Art.448**, banks are required to:

1. Disclose EVE sensitivity under six standardised interest rate shock scenarios
2. Apply the **supervisory outlier test**: if Net EVE (post-hedge) > 15% of Tier 1 capital under any scenario, the bank is classified as an **outlier institution** — a regulatory red flag requiring management action
3. Report the contribution of hedging derivatives to EVE risk reduction (Pillar 3 Table IRRBB3)

The hedge instrument used is a **receive-fixed / pay-floating Interest Rate Swap (IRS) overlay** — the bank receives the fixed rate and pays the floating rate. This converts duration-long fixed-rate asset exposure into floating-rate exposure, reducing EVE sensitivity to rising rates.

---

## 3. Key Parameters

| Parameter | Value | Source |
|---|---|---|
| Tier 1 Capital | €132,173m | Engine!D145 (2025A: CET1 €109,924m + AT1 €22,249m) |
| Hedge Ratio | 55% | Pillar 3 2025, Section 5 IRRBB Table IRRBB3 |
| Base PVBP | −€194.509m/bp | Section 14 (duration-weighted, all buckets) |
| Outlier Threshold | 15% of Tier 1 | CRR Art.448 + EBA/GL/2022/14 para 114 |
| Reference Year | 2025A | — |

**Six Basel Standard Shock Scenarios:**

| # | Scenario | Short Rates | Long Rates |
|---|---|---|---|
| 1 | Parallel Up | +200bp | +200bp |
| 2 | Parallel Down | −200bp | −200bp |
| 3 | Steepener | −90bp | +90bp |
| 4 | Flattener | +90bp | −90bp |
| 5 | Short Rate Up | +250bp | 0bp |
| 6 | Short Rate Down | −250bp | 0bp |

---

## 4. Methodology

### Formula Chain

```
Gross EVE    = Net EVE  ÷  (1 − hedge_ratio)    →  full exposure before IRS
Hedge Offset = Gross EVE × hedge_ratio            →  portion absorbed by IRS swaps
Net EVE      = Gross EVE × (1 − hedge_ratio)      →  residual after hedge
Net EVE/T1   = Net EVE  ÷  Tier 1 Capital         →  regulatory outlier metric
```

### Why Gross Up from Net?

The model reports **Net EVE** (post-hedge) in Section 4 / Section 14. To reconstruct the full decomposition, we gross up using the known hedge ratio:

```
Gross EVE = Net EVE / (1 − 0.55) = Net EVE / 0.45
```

This is consistent with **Pillar 3 Table IRRBB3** methodology, where gross and net EVE are disclosed separately to show hedge contribution.

### IRS Overlay Mechanics

The bank runs a **receive-fixed / pay-floating IRS** programme:
- The bank's assets are **duration-long** (loans avg ~2y, securities avg ~4.5y)
- Liabilities are largely **short/overnight** (deposits)
- This creates a structural **duration gap** — rising rates destroy EVE
- The receive-fixed IRS offsets fixed-rate asset duration: the bank receives fixed cash flows from the swap that partially compensate for the mark-to-market loss on fixed-rate assets when rates rise
- **55% hedge ratio** = 55% of gross EVE exposure is neutralised by the IRS book

### IRS Notional Estimate

```
Estimated Notional ≈ |PVBP_gross| × 10,000 × hedge_ratio / avg_swap_duration
                   ≈ €428bn  (Section 18 proxy, consistent with Pillar 3 disclosure)
```

---

## 5. Key Results

### Hedge Effectiveness Table

| Scenario | Gross EVE (€m) | Hedge Offset (€m) | Net EVE (€m) | Net EVE / T1 | Outlier? |
|---|---|---|---|---|---|
| Par Up +200bps | 38,901.86 | 21,396.02 | 17,505.84 | **13.24%** | Within limit |
| Par Down −200bps | 33,066.58 | 18,186.62 | 14,879.96 | 11.26% | Within limit |
| Steepener +90/−90bps | 17,820.64 | 9,801.35 | 8,019.29 | 6.07% | Within limit |
| Flattener −90/+90bps | 17,820.64 | 9,801.35 | 8,019.29 | 6.07% | Within limit |
| Short Rate Up +250bps | 437.22 | 240.47 | 196.75 | 0.15% | Within limit |
| Short Rate Down −250bps | 371.64 | 204.40 | 167.24 | 0.13% | Within limit |

**Result: ALL 6 SCENARIOS WITHIN OUTLIER LIMIT — IRS hedge is effective**

### Key Insights

**1. The hedge is critical on Parallel Up**
Without the 55% IRS overlay, the Par Up gross EVE of €38,902m would represent **29.4% of Tier 1** — a serious regulatory outlier. The hedge brings it to 13.24% — just inside the 15% threshold. The bank has minimal headroom; reducing the hedge ratio below ~53% would trigger outlier status.

**2. Par Down is the second-most sensitive scenario**
Falling rates increase the value of fixed-rate assets, but also increase liability costs. Gross EVE under Par Down = €33,067m (25.0% of Tier 1 gross). The hedge reduces this to 11.26% net.

**3. Short rate scenarios carry minimal EVE risk**
Short Rate Up/Down produce gross EVE of only ~€400m (0.3% of Tier 1 gross). These scenarios shift only the short end of the yield curve, leaving long-duration assets/liabilities largely unaffected.

**4. Steepener and Flattener are symmetric**
Both produce identical gross EVE (€17,821m), reflecting the symmetric ±90bp shock applied to long and short rates respectively.

---

## 6. Cross-Check vs Excel Section 18

Line-by-line verification of all 18 output cells against Section 18 of the Excel model:

| Scenario | Gross Diff (€m) | Net Diff (€m) | Status |
|---|---|---|---|
| Par Up +200bps | 0.0020 | 0.0001 | PASS |
| Par Down −200bps | 0.0027 | 0.0002 | PASS |
| Steepener +90/−90bps | 0.0048 | 0.0002 | PASS |
| Flattener −90/+90bps | 0.0048 | 0.0002 | PASS |
| Short Rate Up +250bps | 0.0015 | 0.0003 | PASS |
| Short Rate Down −250bps | 0.0043 | 0.0001 | PASS |

✅ All 18 checks passed — differences < €0.005m (rounding only)

---

## 7. Limitations

- Static balance sheet — hedge ratio assumed constant; dynamic re-hedging not modelled
- IRS notional is a proxy estimate — actual notional schedule requires full swap cashflow data
- Duration-based PVBP method used (EBA/GL/2022/14 Annex II simplified approach); full cashflow discounting per CRR Art.448 would give a more precise gross EVE
- Hedge effectiveness testing (IAS 39 / IFRS 9 80–125% corridor) not included — this is an economic hedge, not necessarily a formal accounting hedge relationship
- Convexity of the IRS book is not modelled

---

## 8. ALM Takeaway

The IRS overlay programme demonstrates that regulatory compliance and income optimisation are not binary choices: by hedging approximately 55% of gross EVE exposure rather than eliminating it entirely, the bank reduces its worst-case Net EVE to 13.24% of Tier 1 — inside the 15% outlier threshold — while preserving the asset-sensitive NII upside quantified in Projects 1 and 2. A 100% hedge would be regulatory overkill, sacrificing the income benefit of rising rates for no additional capital benefit. The residual 13.24% represents a deliberate risk appetite decision approved at ALCO level, balancing the ECB's EVE supervisory expectation against the Treasury desk's mandate to optimise net interest income across the rate cycle.

---

## 9. Files

| File | Description |
|---|---|
| `Hedge_Effectiveness.ipynb` | Main notebook (8 cells) |
| `Hedge_Effectiveness_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source Excel model (Section 18) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
*Methodology: EBA/GL/2022/14 Annex I | CRR Art.448 (simplified PVBP implementation)*
---
