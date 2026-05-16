# Project 3 of 12 — LCR / NSFR Liquidity Calculator
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview
This project implements a professional Basel III Liquidity Risk Calculator in Python, computing both the Liquidity Coverage Ratio (LCR) and Net Stable Funding Ratio (NSFR) across four macro scenarios. The model is calibrated to the balance sheet of a major European G-SIB (Q4 2025A actuals) and cross-validated against an Excel master model with a difference of −0.01% on LCR and 0.00% on NSFR. A key feature is a scenario-sensitive Non-Maturity Deposit (NMD) behavioural model — rather than the static 70/30 deposit split used in simplified models.

## 2. Regulatory Context

| Ratio | Regulation | Minimum |
|---|---|---|
| LCR | **Delegated Regulation (EU) 2022/786** (amending 2015/61) | ≥ 100% |
| NSFR | **CRR Art. 428a–428at (CRR2)** | ≥ 100% |

NMD behavioural modelling is required under **EBA/GL/2022/14** — a static deposit split produces materially incorrect NSFR results under stress.

## 3. Balance Sheet Summary

All figures in EUR millions. Reference year: 2025A.

**Assets**

| Item | Volume (€m) | LCR Treatment | NSFR RSF Factor |
|---|---|---|---|
| Cash & CB Reserves | 211,330 | Level 1 HQLA | 0% (Art.428q) |
| Government Bonds | 110,237 | Level 1 HQLA | 5% (Art.428r) |
| Corporate Bonds | 42,870 | Level 2A HQLA | 15% (Art.428s) |
| Loans to Customers | 897,358 | 10% outflow (commitments) | 76.25% blended (Art.428t/u) |
| Interbank Loans | 26,259 | 100% inflow | 10% (Art.428u) |
| Insurance Assets | 305,471 | Not HQLA | 100% (Art.428ab) |
| Trading Assets | 870,245 | Not HQLA | Mixed (Art.428r/ag/ab) |

**Liabilities**

| Item | Volume (€m) | LCR Outflow Rate | NSFR ASF Factor |
|---|---|---|---|
| Customer Deposits | 1,075,564 | 5–10% (NMD-adjusted) | 80–90% (NMD-adjusted) |
| Interbank Funding | 69,938 | 100% (Art.31) | 0% (Art.428p) |
| Repo Funding | 357,947 | 0–15% (by collateral) | 10% (Art.428s) |
| Bonds Issued | 173,933 | 25% (Art.27) | 100% (Art.428n) |
| Subordinated Debt | 34,468 | — | 50% (Art.428o) |
| Equity | 132,173 | — | 100% (Art.428d) |

## 4. Methodology

**LCR:**
```
LCR = HQLA / Net Cash Outflows (30d) ≥ 100%
```
HQLA = Level 1 (0% haircut) + Level 2A (15% haircut). Net Outflows = Gross Outflows − min(Inflows, 75% × Outflows). The 75% inflow cap (Art.33) is mandatory.

**NSFR:**
```
NSFR = Available Stable Funding (ASF) / Required Stable Funding (RSF) ≥ 100%
```
ASF is weighted by funding stability (0–100% per CRR Art.428d–428s). RSF is weighted by liquidity need of each asset class (0–100% per CRR Art.428q–428ab).

**NMD Behavioural Model — Scenario-Sensitive Stable Deposit %:**

| Scenario | Stable % | Rationale |
|---|---|---|
| Base | 70% | Normal environment |
| Rate Hike | 65% | Rate alternatives attract depositors |
| Rate Cut | 72% | Low-rate alternatives keep deposits sticky |
| Stress | 50% | Significant reclassification to non-core |

## 5. Key Results

**LCR — All Scenarios Pass:**

| Scenario | HQLA (€m) | Net Outflows (€m) | LCR | Status |
|---|---|---|---|---|
| Base | 364,437 | 234,540 | 155.4% | ✅ PASS |
| Rate Hike | 364,437 | 236,766 | 153.9% | ✅ PASS |
| Rate Cut | 364,437 | 238,363 | 152.9% | ✅ PASS |
| Stress | 364,437 | 245,700 | 148.3% | ✅ PASS |

The bank holds a substantial HQLA buffer of €364bn, dominated by Level 1 assets (€322bn).

**NSFR — Stress Scenario Breaches:**

| Scenario | ASF (€m) | RSF (€m) | NSFR | Status |
|---|---|---|---|---|
| Base | 1,318,269 | 1,290,227 | 102.2% | ✅ PASS |
| Rate Hike | 1,308,105 | 1,283,384 | 101.9% | ✅ PASS |
| Rate Cut | 1,325,163 | 1,297,069 | 102.2% | ✅ PASS |
| **Stress** | **1,273,364** | **1,276,542** | **99.8%** | **❌ BREACH** |

Under stress, deposit reclassification (NMD: 50% stable) compresses ASF by €45bn, pushing NSFR below the regulatory floor. A static 70/30 model would produce a false NSFR pass.

## 6. Cross-Check vs Excel

| Metric | Excel 2025A | Python 2025A | Difference |
|---|---|---|---|
| LCR | 155.44% | 155.43% | −0.01% ✅ |
| NSFR | 101.98% | 101.98% | 0.00% ✅ |

## 7. ALM Takeaway

While the bank maintains a comfortable LCR buffer in both base and stress scenarios — reflecting adequate short-term liquidity management — the NSFR tells a different story: the base ratio of 102.2% leaves virtually no headroom, and the stress scenario produces a regulatory breach at 99.8%. This signals a structural funding vulnerability: the bank is over-reliant on short-term or behavioural deposits to fund longer-dated assets. The practical response would be to extend the liability maturity profile through additional MREL-eligible debt issuance or long-term covered bonds — an action the Funding desk would typically model against the cost of carry before escalating to ALCO.

## 8. Files

| File | Description |
|---|---|
| `LCR_NSFR_Calculator.ipynb` | Main notebook (9 cells) |
| `LCR_NSFR_Calculator_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source balance sheet data — Major European G-SIB ALM Model (2025A) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
---
