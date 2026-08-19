# Phase 2 — Data & AIML Pipeline

## Overview

Phase 2 transforms the generated retail inventory data into an
ML-based demand forecasting and inventory intelligence pipeline.

## Dataset

The synthetic dataset contains:

- 20 stores
- 100 products
- 2,000 store-product inventory records
- 1,462,000 sales records

After feature engineering, 1,406,000 records were available for ML.

## Exploratory Data Analysis

The following analyses were performed:

- Daily sales demand
- Monthly sales demand
- Sales by product category
- Sales by store
- Weekday demand patterns
- Promotion impact
- Holiday impact
- Feature correlation
- Missing-value analysis

All four source datasets contained zero missing values.

## Feature Engineering

The forecasting dataset includes:

- Calendar features
- Store and product identifiers
- Price
- Promotion indicators
- Holiday/weekend indicators
- 1-day demand lag
- 7-day demand lag
- 14-day demand lag
- 28-day demand lag
- 7-day rolling mean
- 14-day rolling mean
- 28-day rolling mean
- 7-day rolling standard deviation
- Price change

## Model Evaluation

A time-based train/validation/test split was used to avoid
future-data leakage.

### Test Results

| Model | MAE | RMSE |
|---|---:|---:|
| 7-Day Average Baseline | 8.0056 | 11.6429 |
| Random Forest | 6.4430 | 9.1095 |
| HistGradientBoosting | 6.3240 | 8.9323 |

HistGradientBoosting achieved the best test performance.

## Forecast Analysis

The selected model generated 184,000 test-period forecasts.

The overall test MAE was 6.3240.

The model's largest observed absolute error was approximately
99 units.

Forecast errors were also analyzed by:

- Product category
- Store
- Prediction direction
- Individual forecast

Fashion had the highest average forecast error among the
categories analyzed.

## Inventory Risk Detection

The forecasting output was combined with current inventory and
safety-stock information.

Risk distribution:

| Risk Level | Count |
|---|---:|
| LOW | 1,419 |
| MEDIUM | 457 |
| HIGH | 124 |

## Inventory Rebalancing

The system identifies stores with inventory shortages and matches
them with stores having safe transferable surplus.

The optimization considers:

- Current stock
- Safety stock
- Forecast demand
- Destination capacity
- Transfer quantity
- Transfer priority

The system generated:

- 124 optimized transfer recommendations
- 11,453 recommended transfer units

## Validation

The transfer recommendations were validated for:

- Self-transfers
- Invalid quantities
- Source-stock violations
- Destination-capacity violations
- Non-high-risk destinations
- Missing source records
- Missing destination records

All validation checks returned zero violations.

## Phase 2 Outcome

Phase 2 establishes the core AIML intelligence pipeline:

Raw Sales Data
→ Feature Engineering
→ Demand Forecasting
→ Forecast Analysis
→ Inventory Risk Detection
→ Transfer Optimization

The resulting models and analytical outputs form the foundation
for the next project phase.