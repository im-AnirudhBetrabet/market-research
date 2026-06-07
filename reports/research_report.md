# Market Factor Research Report

## Dataset Summary

Analysis Timestamp: 2026-06-07 12:22:38.249841
Observation Count: 2154
Date Range: 2017-07-12 00:00:00 -> 2026-06-02 00:00:00

## Executive Summary

Strongest factor: Gift Return
Nifty correlation: 0.457

## Factor Ranking (Nifty Gap)

| Rank | Factor      | Correlation | Accuracy |
|------|-------------|------------:|---------:|
| 1    | Gift Return |       0.457 |   63.51% |
| 2    | VIX Return  |      -0.446 |   60.72% |

# Gift Return

## Correlation Analysis

Nifty Gap: 0.457
Sensex Gap: 0.436

## Directional Analysis

Nifty Accuracy: 63.51%
Sensex Accuracy: 61.23%

## Bucket Analysis (Nifty)

| Bucket        | Observations | Accuracy |
|---------------|-------------:|---------:|
| 0.00% - 0.20% |          384 |   54.43% |
| 0.20% - 0.50% |          600 |   58.33% |
| 0.50% - 1.00% |          664 |   67.32% |
| 1.00% - 1.50% |          275 |   66.55% |
| 1.50% - 2.00% |          139 |   74.10% |
| 2.00% - 3.00% |           59 |   76.27% |
| 3.00%+        |           33 |   93.94% |

## Bucket Analysis (Sensex)

| Bucket        | Observations | Accuracy |
|---------------|-------------:|---------:|
| 0.00% - 0.20% |          384 |   52.60% |
| 0.20% - 0.50% |          600 |   57.50% |
| 0.50% - 1.00% |          664 |   64.76% |
| 1.00% - 1.50% |          275 |   61.09% |
| 1.50% - 2.00% |          139 |   71.94% |
| 2.00% - 3.00% |           59 |   74.58% |
| 3.00%+        |           33 |   90.91% |

## Lag Analysis (Nifty)

| Feature           | Correlation |
|-------------------|------------:|
| gift_return       |       0.457 |
| gift_return_lag1  |       0.189 |
| gift_return_lag2  |       0.070 |
| gift_return_lead1 |       0.038 |

## Lag Analysis (Sensex)

| Feature           | Correlation |
|-------------------|------------:|
| gift_return       |       0.436 |
| gift_return_lag1  |       0.182 |
| gift_return_lag2  |       0.055 |
| gift_return_lead1 |       0.028 |

# VIX Return

## Correlation Analysis

Nifty Gap: -0.446
Sensex Gap: -0.442

## Directional Analysis

Nifty Accuracy: 60.72%
Sensex Accuracy: 59.29%

## Bucket Analysis (Nifty)

| Bucket        | Observations | Accuracy |
|---------------|-------------:|---------:|
| 0.00% - 0.20% |           74 |   43.24% |
| 0.20% - 0.50% |          152 |   46.05% |
| 0.50% - 1.00% |          202 |   54.95% |
| 1.00% - 1.50% |          215 |   54.88% |
| 1.50% - 2.00% |          190 |   60.53% |
| 2.00% - 3.00% |          374 |   57.49% |
| 3.00%+        |          947 |   68.32% |

## Bucket Analysis (Sensex)

| Bucket        | Observations | Accuracy |
|---------------|-------------:|---------:|
| 0.00% - 0.20% |           74 |   52.70% |
| 0.20% - 0.50% |          152 |   48.03% |
| 0.50% - 1.00% |          202 |   56.44% |
| 1.00% - 1.50% |          215 |   52.09% |
| 1.50% - 2.00% |          190 |   55.26% |
| 2.00% - 3.00% |          374 |   56.95% |
| 3.00%+        |          947 |   65.58% |

## Lag Analysis (Nifty)

| Feature          | Correlation |
|------------------|------------:|
| vix_return       |      -0.446 |
| vix_return_lag1  |      -0.058 |
| vix_return_lag2  |      -0.087 |
| vix_return_lead1 |      -0.036 |

## Lag Analysis (Sensex)

| Feature          | Correlation |
|------------------|------------:|
| vix_return       |      -0.442 |
| vix_return_lag1  |      -0.065 |
| vix_return_lag2  |      -0.073 |
| vix_return_lead1 |      -0.025 |
