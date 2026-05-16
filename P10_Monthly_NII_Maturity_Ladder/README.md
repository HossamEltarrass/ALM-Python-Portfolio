# Project 10 of 12 — Monthly NII Simulation & Maturity Ladder
**Author:** Hossam Eltarrass
**Institution:** Major European G-SIB (Anonymised)
**Series:** ALM Python Portfolio | ALM Intern
**Date:** May 2026

---

## 1. Overview

This project implements two related ALM tools that together answer how income arrives over time and how long the bank can survive a liquidity stress event. It is the tenth project in a Python ALM portfolio built to demonstrate junior analyst capability in asset-liability management.

All figures are in **EUR millions (€m)**.

---

## 2. Regulatory Context

| Measure | Regulation | Requirement |
|---|---|---|
| Monthly NII repricing | **EBA/GL/2022/14** | Scenario-specific repricing lag modelling required |
| Maturity Ladder / LCR | **Del. Reg. (EU) 2022/786** | 30-day survival horizon minimum |
| ILAAP survival horizon | **EBA/GL/2021/05** | Internal threshold typically ≥ 3 months |

---

## 3. Balance Sheet Summary

All figures in EUR millions. Reference year: 2025A / 2026F.

### Assets

| Item | Balance (€m) | Base Rate | Reprice Freq | Beta |
|---|---|---|---|---|
| Cash & CB Reserves | 211,330 | 2.50% | Monthly | 1.0 |
| Loans to Customers | 897,358 | 3.80% | Quarterly | 0.9 |
| Interbank Loans | 26,259 | 3.10% | Monthly | 1.0 |
| Securities Portfolio | 153,107 | 3.00% | Fixed | 0.0 |

### Liabilities

| Item | Balance (€m) | Base Rate | Reprice Freq | Beta |
|---|---|---|---|---|
| Customer Deposits | 1,075,564 | 0.50% | Quarterly | 0.4 |
| Interbank Funding | 69,938 | 3.10% | Monthly | 1.0 |
| Repo Funding | 357,947 | 2.415% | Monthly | 1.0 |
| Bonds Issued | 173,933 | 3.25% | Fixed | 0.0 |
| Subordinated Debt | 34,468 | 2.50% | Fixed | 0.0 |

---

## 4. Methodology

### Section 12 — Monthly Forward NII Simulation

Unlike Project 1 (which applied a single annual rate shock), Section 12 simulates NII month by month. The key new concept is **repricing lag** — the delay between when the ECB moves rates and when that change flows through to each instrument.

**Effective rate formula:**

```
effective_rate = base_rate + (market_rate_change) × beta
```

`market_rate_change` is applied only at the instrument's repricing frequency:

| reprice_freq | Meaning | Instruments |
|---|---|---|
| 0 | Fixed — rate never changes | Bonds Issued, Subordinated Debt, Securities Portfolio |
| 1 | Monthly — resets every month | Cash & CB Reserves, Interbank Loans, Repo Funding, Interbank Funding |
| 3 | Quarterly — resets Jan/Apr/Jul/Oct | Loans to Customers, Customer Deposits |

**Monthly NII formula:**

```
Asset Income(m)    = Σ balance × effective_rate × (days_in_month / 365)
Liability Cost(m)  = Σ balance × effective_rate × (days_in_month / 365)
Monthly NII(m)     = Asset Income(m) − Liability Cost(m)
```

**Rate Scenarios:**

| Scenario | Description | Year-end DFR |
|---|---|---|
| Base | ECB holds at 2.25% all year | 2.25% |
| ECB Cut | −25bp in March, −25bp in June | 1.75% |
| ECB Hike | +50bp in March | 2.75% |

### Section 13 — Maturity Ladder & Liquidity Survival Horizon

The maturity ladder maps every balance sheet item to the time bucket in which it matures, producing contractual cash inflows (assets) and outflows (liabilities) by bucket. Time buckets: O/N → 1W → 2W → 1M → 2M → 3M → 6M → 9M → 12M

**Survival horizon:** the last time bucket where the cumulative net gap (running sum of inflows − outflows) remains non-negative.

**Stress Scenario Assumptions:**

| Stress Driver | Assumption | Additional Outflow |
|---|---|---|
| Repo frozen | 30% of €357,947m cannot be rolled | €107,384m (O/N–1M) |
| Interbank frozen | 50% of €69,938m cannot be rolled | €34,969m (1W–1M) |
| Deposit flight | 10% additional withdrawal above base | €107,556m (1M–6M) |

---

## 5. Key Results

### Section 12 — Annual NII by Scenario

| Scenario | Annual NII (€m) | vs Base (€m) |
|---|---|---|
| Base | **22,085** | — |
| ECB Cut | < Base | Negative |
| ECB Hike | > Base | Positive |

*Exact scenario deltas are computed dynamically at runtime.*

**Structural finding:** The bank is asset-sensitive. A rate hike increases annual NII more than an equivalent cut reduces it. The repricing asymmetry is visible month by month: asset income moves first, deposit costs follow only at the quarterly reset.

### Section 13 — Survival Horizons

| Scenario | Survival Horizon | Cumulative Gap at Horizon |
|---|---|---|
| Base | **9M** | +€3,602m (barely positive — turns negative at 12M) |
| Stress | **2M** | Turns negative between 2M and 3M buckets |

The 7-month gap between Base (9M) and Stress (2M) survival horizons is entirely explained by the wholesale market rollability assumption. The repo book (€358bn) represents the core liquidity vulnerability — cheap and efficient in normal times but unavailable exactly when needed most.

| Measure | Threshold | This Bank |
|---|---|---|
| Basel LCR minimum | 30 days | Satisfied (2M > 30 days) |
| Internal ILAAP threshold | 3 months | Close — 2M stress horizon approaches limit |

---

## 6. Cross-Check vs Excel

| Metric | Excel | Python | Difference |
|---|---|---|---|
| Base NII (annual sum of 12 months) | €22,085m | €22,085m | €0 ✅ |

Base scenario: sum of 12 monthly NII values = **€22,085m** — matches Project 1 (NII Scenario Tool) annual Base NII exactly.

---

## 7. Limitations

- Static balance sheet — no new lending, deposit growth, or issuance modelled
- Behavioural deposit maturity is simplified (40% due within 12M — no granular NMD model)
- Repo and interbank stress haircuts are illustrative; real LCR uses Basel-prescribed runoff rates
- Loans to Customers maturity profile is approximated — no prepayment or CPR model applied (see Project 7)
- Rate scenarios are stepwise (discrete ECB meetings) — no continuous path modelling

---

## 8. ALM Takeaway

The maturity ladder fills the analytical gap between the LCR's 30-day stress window and the NSFR's 1-year structural view, giving Treasury the monthly cash flow profile needed to manage liquidity dynamically rather than at fixed regulatory horizons. The base survival horizon of 9 months provides comfortable runway, but the stress horizon of 2 months underscores that the bank's liquidity resilience is highly assumption-dependent: under stressed deposit outflows, the funding gap accelerates sharply. In practice, a 2-month stress horizon would trigger the bank's Contingency Funding Plan well in advance — typically at the 6-month early warning threshold — with pre-positioned central bank collateral and committed credit lines activated before the survival boundary is breached.

---

## 9. Files

| File | Description |
|---|---|
| `Monthly_NII_Maturity_Ladder.ipynb` | Main notebook (11 cells) |
| `Monthly_NII_Maturity_Ladder_README.md` | This file |
| `MAJOR_EUROPEAN_GSIB_ALM_Model.xlsx` | Source Excel model (Sections 12–13) |

---
*Part of a 12-project ALM Python portfolio built on a Major European G-SIB balance sheet (2025A/2026F). All data anonymised.*
*Methodology: ALM best practice — repricing lag simulation + contractual maturity ladder*
---
