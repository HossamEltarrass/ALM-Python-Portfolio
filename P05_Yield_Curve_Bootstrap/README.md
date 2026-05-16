# Project 5 of 12 — Yield Curve Bootstrap
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview
This project bootstraps the EUR zero (spot) rate curve from raw market inputs, replicates the YieldCurve sheet of the ALM model exactly, and applies four IRRBB standardised shock scenarios from EBA/GL/2022/14. Working from just four market anchor points, the bootstrap iteratively solves discount factors from short to long maturities, then derives spot and forward rates. Reference year: 2026F.

## 2. Regulatory Context
Shock scenarios are defined by **EBA/GL/2022/14 IRRBB Guidelines**: Parallel Up/Down (+/−200bps), Steepener, and Flattener. The bootstrapped curve feeds directly into Projects 1 (NII repricing rates), 2 (EVE/IRRBB), and 4 (bond YTMs). The Parallel Up +200bps scenario corresponds to Basel Scenario 1 of the mandatory outlier test.

## 3. Market Inputs

Four raw market inputs — everything else is derived:

| Parameter | Value | Source |
|---|---|---|
| ECB Policy Rate (DFR) | 2.25% | Engine sheet E14, 2026F |
| 3M Euribor | 2.35% | Engine sheet E15, 2026F |
| 5Y EUR Swap Rate | 2.70% | Engine sheet E16, 2026F |
| 10Y EUR Swap Rate | 2.55% | Engine sheet E17, 2026F |

Curve shape: slightly inverted at the long end (5Y 2.70% > 10Y 2.55%), reflecting market expectations that rates will decline over the long run in the 2026F planning horizon.

## 4. Methodology

**Step 1 — Par Rate Interpolation:** Piecewise linear interpolation between the four market anchors fills par rates for all annual tenors (1Y–10Y).

**Step 2 — Bootstrap Formula:** For annual par swap rates, the price of a par swap equals 1:
```
DF(T) = (1 − c_T × Σ DF(1..T−1)) / (1 + c_T)
```
Applied iteratively: 1Y → 2Y → 3Y → ... → 10Y.

**Step 3 — Spot and Forward Rates:**
```
Spot Rate:    z(T) = (1/DF(T) − 1) / T          [simple interest]
Forward Rate: f(T1→T2) = (DF(T1)/DF(T2) − 1) / (T2 − T1)
```

**Step 4 — IRRBB Shocks:** Applied additively to base spot rates. Steepener and Flattener are neutral at 5Y — the curve rotates around that point.

| Scenario | Short End | Long End |
|---|---|---|
| Parallel Up | +200bps | +200bps |
| Parallel Down | −200bps | −200bps |
| Steepener | +90bps | −90bps |
| Flattener | −90bps | +90bps |

## 5. Key Results

**Bootstrapped Zero Curve (Base Case, 2026F):**

| Tenor | Par Rate | Discount Factor | Spot Rate | Fwd Rate→next |
|---|---|---|---|---|
| 1Y | 2.4053% | 0.97651231 | 2.4053% | 2.5545% |
| 2Y | 2.4789% | 0.95218852 | 2.5106% | 2.9432% |
| 3Y | 2.5526% | 0.92710188 | 2.6210% | 3.1459% |
| 4Y | 2.6263% | 0.90132594 | 2.7369% | 3.1906% |
| 5Y | 2.7000% | 0.87493430 | 2.8589% | 2.4920% |
| 6Y | 2.6700% | 0.85353455 | 2.8600% | 2.4894% |
| 7Y | 2.6400% | 0.83318416 | 2.8602% | 2.4834% |
| 8Y | 2.6100% | 0.81383861 | 2.8593% | 2.4754% |
| 9Y | 2.5800% | 0.79545564 | 2.8571% | 2.4658% |
| 10Y | 2.5500% | 0.77799519 | 2.8535% | N/A |

The bootstrapped spot curve rises from 2.41% at 1Y, **peaks at 7Y (2.860%)**, then eases slightly to 2.854% at 10Y. Zero rates are systematically above par rates at every tenor — the bootstrap strips out coupon reinvestment, revealing the true time-value of money at each maturity. The discount factor falls from 0.9765 at 1Y to 0.7780 at 10Y.

## 6. Cross-Check vs Excel

Python results compared against the YieldCurve sheet of the Excel model:

| Metric | Max Absolute Error |
|---|---|
| Discount Factors | < 1e-6 |
| Spot Rates | < 1e-6 |

✅ Cross-check passed — Python replicates the Excel model exactly.

## 7. ALM Takeaway

The bootstrapped spot curve is the backbone of the entire ALM model — every discount factor, FTP rate, and EVE calculation in Projects 4, 6, and 9 depends on it being internally consistent. The mild hump at 7Y, where spot rates peak at 2.860% before easing to 2.854% at 10Y, reflects market pricing of eventual ECB rate cuts: the 10Y swap trades below the 7Y because the market embeds a rate reduction into the long end. For the FTP desk, this inversion compresses the liquidity premium on 10Y mortgages relative to 7Y — a subtle but real pricing signal that affects the profitability of long-dated fixed-rate lending.

## 8. Files

| File | Description |
|---|---|
| `Yield_Curve_Bootstrap.ipynb` | Main notebook |
| `Yield_Curve_Bootstrap_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source Excel model (YieldCurve sheet) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
---
