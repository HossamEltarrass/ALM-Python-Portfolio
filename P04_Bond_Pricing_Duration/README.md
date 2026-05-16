# Project 4 of 12 — Bond Pricing & Duration Calculator
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview
This project builds a bond-level pricing and interest rate sensitivity tool for the securities portfolio of a major European G-SIB. While the master balance sheet model tracks securities as a single aggregate line (€153,107m at a blended yield), this notebook prices each bond individually and decomposes rate risk by instrument, maturity, and bond type. This is the analysis a fixed income or ALM analyst runs inside the securities book before hedging decisions, IRRBB stress reporting, and FRTB capital calculations.

> **Simplifying assumption:** All bonds are priced at par in this model. In practice, bonds trade at a premium or discount to par depending on current market yields versus their coupon rate.

## 2. Regulatory Context
- **IRRBB (EBA/GL/2022/14)** — EVE sensitivity requires bond-level DV01 aggregation; +200bps is Scenario 1 of the mandatory outlier test
- **FRTB (CRR2 / Basel IV)** — DV01 by maturity bucket feeds the Standardised Approach capital calculation
- **IFRS 9** — Duration matching underpins fair value hedge effectiveness testing

## 3. Balance Sheet Summary

10 representative bonds covering the full maturity spectrum and the G-SIB's 72/28 government/non-government split. All figures in EUR millions.

| # | Bond | Type | Notional (€m) | Maturity | YTM |
|---|------|------|--------------|----------|-----|
| 1 | DE Bund 2Y | Government | 25,000 | 2yr | 2.51% |
| 2 | FR OAT 5Y | Government | 40,000 | 5yr | 2.86% |
| 3 | IT BTP 10Y | Government | 30,000 | 10yr | 2.85% |
| 4 | ES Bono 30Y | Government | 15,237 | 30yr | 3.15% |
| 5 | Corp IG 3Y | Corporate | 10,000 | 3yr | 3.10% |
| 6 | Corp IG 7Y | Corporate | 12,000 | 7yr | 3.30% |
| 7 | Corp IG 10Y | Corporate | 10,621 | 10yr | 3.40% |
| 8 | Covered 2Y | Covered Bond | 4,500 | 2yr | 2.70% |
| 9 | Covered 5Y | Covered Bond | 4,686 | 5yr | 3.05% |
| 10 | EIB Supra 5Y | Supranational | 1,063 | 5yr | 2.90% |
| | **TOTAL** | | **153,107** | | |

Yields are derived from the bootstrapped EUR spot rate curve (Project 5) plus instrument-specific credit spreads.

## 4. Methodology

All functions are built from scratch using underlying financial mathematics — no external bond pricing libraries.

- **Price:** PV of all future cash flows discounted at YTM using the DCF formula
- **Macaulay Duration:** Weighted average time to receive cash flows (years)
- **Modified Duration:** % price change per 1% move in yield (ModDur = MacDur / (1 + y))
- **DV01/PVBP:** € P&L for a 1 basis point move in yield (DV01 = ModDur × Price × 0.0001 × notional/100)
- **Convexity:** Second-order curvature correction using the full Taylor expansion: ΔP/P ≈ −ModDur × Δy + ½ × Convexity × (Δy)²
- **Scenario Analysis:** Full reprice across ±25, ±50, ±100, ±200bps parallel yield shifts

## 5. Key Results

| Metric | Value |
|---|---|
| Portfolio Total | **€153,107m** |
| Portfolio DV01 | **€100.88m per basis point** |
| Weighted Avg. Modified Duration | **6.59 years** |
| Weighted Avg. Convexity | **85.38** |
| P&L at +100bps | **−€9,500m** |
| P&L at +200bps | **−€17,900m** |
| P&L at −200bps | **+€23,200m** |

**Risk concentration:**
- **ES Bono 30Y** — 10% of portfolio by value, **29.0% of total DV01**
- **IT BTP 10Y** — 20% of portfolio by value, **25.6% of total DV01**
- Government bonds (72% of MV) account for **77.6% of DV01** due to longer average duration

**Convexity benefit:** At +200bps, the duration-only estimate predicts a loss of €20,176m. The exact full reprice shows a loss of €17,900m. Convexity saves €2,276m — an 11% reduction in expected loss that a linear model misses.

## 6. Cross-Check vs Excel

The +200bps P&L of −€17,900m is directly comparable to the EVE shock in Project 2 (−€22,345m on the full balance sheet). The securities book accounts for approximately 80% of total balance sheet EVE sensitivity, confirming it is the dominant source of interest rate risk in this G-SIB.

| Scenario | Portfolio P&L (€m) | % of Book |
|---|---|---|
| −200bps | +23,200 | +15.2% |
| +100bps | −9,500 | −6.2% |
| +200bps | −17,900 | −11.7% |

## 7. ALM Takeaway

A DV01 of €100.88m/bp means the securities portfolio generates over €100m of mark-to-market gain or loss for every basis point move in rates — a material exposure on a book of €153,107m. The convexity benefit of €2,276m at +200bps illustrates why duration alone underestimates hedge requirements for larger shocks. In practice, Treasury must choose between reducing this sensitivity through outright bond sales — which crystallise unrealised losses on the P&L — or through receive-fixed IRS overlays that reduce duration at a carry cost. This trade-off is exactly what feeds into the hedge sizing decision modelled in Project 9.

## 8. Files

| File | Description |
|---|---|
| `Bond_Pricing_Duration.ipynb` | Main notebook |
| `Bond_Pricing_Duration_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source balance sheet data — Major European G-SIB ALM Model (2025A) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
---
