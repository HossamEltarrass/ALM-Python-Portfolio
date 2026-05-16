# Project 6 of 12 — Funds Transfer Pricing (FTP) Framework
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview
This project implements the internal Funds Transfer Pricing (FTP) framework used by a major European G-SIB to decompose total bank NII across business units. Every asset and liability is priced through the ALM desk using a tenor-matched internal curve. This isolates interest rate risk in the ALM desk and leaves each business unit with a clean, stable margin that reflects only its customer franchise — enabling the ALCO and CFO to measure the true profitability of each business line.

## 2. Regulatory Context
FTP framework methodology is governed by **BCBS 239** (risk data aggregation and risk reporting principles) and **EBA internal governance guidelines**, which require banks to have a robust internal pricing mechanism that fully attributes NII. The liquidity premium component is calibrated to the bank's own funding costs — approximately 55bps at the 5Y tenor (2025A CDS level).

## 3. Balance Sheet Summary

All figures in EUR millions. Reference year: 2026F. Base rates (1Y–10Y) sourced directly from the bootstrapped zero curve in Project 5.

**Key Inputs:**

| Input | Value | Source |
|-------|-------|--------|
| ECB DFR (Overnight base) | 2.25% | Engine sheet |
| 3M Euribor | 2.35% | Engine sheet |
| 1Y–10Y base rates | From Project 5 bootstrap | YieldCurve sheet |
| Liquidity premium | 0–50 bps across tenors | Section 15 |
| Mortgage product rate | 4.50% | Section 15 |
| Mortgage book balance | €277,284m | Section 15 |
| Deposit rate paid | 0.40% | Section 15 |
| NMD balance | €1,102,453m | Section 15 |

## 4. Methodology

The ALM desk acts as an internal central bank:
- Every **loan** originated → the lending desk pays an FTP charge to the ALM desk and retains only the spread above it
- Every **deposit** taken → the deposit desk receives an FTP credit from the ALM desk and retains the spread above what it pays customers

Key equations:
```
FTP Rate         = Base Rate (spot) + Liquidity Premium (bps) / 100
Lending NIM      = Customer Rate − FTP Rate at matched tenor
Deposit Margin   = FTP Credit − Rate paid to customers
NII Contribution = Margin × Book Balance
```

**FTP Curve — 8 Tenors:**

| Tenor | Base Rate | Liq. Premium | FTP Rate |
|-------|-----------|--------------|----------|
| Overnight | 2.2500% | 0 bps | 2.2500% |
| 1 Month | 2.2800% | 5 bps | 2.3300% |
| 3 Months | 2.3500% | 10 bps | 2.4500% |
| 6 Months | 2.3700% | 15 bps | 2.5200% |
| 1 Year | 2.4053% | 20 bps | 2.6053% |
| 2 Year | 2.5106% | 25 bps | 2.7606% |
| 5 Year | 2.8589% | 35 bps | **3.2089%** |
| 10 Year | 2.8535% | 50 bps | 3.3535% |

## 5. Key Results

| Desk | Balance | Net Margin | NII Contribution |
|------|---------|------------|-----------------|
| Mortgage Desk | €277,284m | 1.2911% | **€3,580m** |
| Retail Deposit Desk | €1,102,453m | 1.85% | **€20,395m** |
| **TOTAL** | | | **€23,975m** |

The deposit franchise margin (€20,395m) is the largest single NII contributor — 85.1% of total FTP-attributed NII. This reflects the structural advantage of a large, sticky retail deposit base in a positive rate environment.

## 6. Cross-Check vs Excel

| Output | Excel (Section 15) | Python | Difference |
|--------|--------------------|--------|------------|
| Mortgage NII | €3,580.1m | €3,580m | €0.1m rounding |
| Deposit NII | €20,395.4m | €20,395m | €0.4m rounding |

Cross-check = **€0** (within rounding). Python replicates the Excel model exactly.

## 7. ALM Takeaway

FTP transforms ALM from a passive risk measurement function into an active internal pricing mechanism. By charging the mortgage desk 3.2089% for 5Y funding and crediting the deposit desk for providing stable cheap liabilities, Treasury ensures each business line bears its true cost of liquidity — preventing cross-subsidisation and making risk-adjusted profitability comparable across the bank. The result that the deposit franchise generates over 85% of total NII (€20,395m of €23,975m) quantifies exactly why deposit stickiness and repricing behaviour are the most strategically important variables in the ALM model — and why they are stress-tested separately in Projects 3, 7, and 10.

## 8. Files

| File | Description |
|------|-------------|
| `ftp_framework.ipynb` | Main notebook — FTP curve, worked examples, chart |
| `FTP_Framework_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source Excel model (Section 15) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
---
