# Market Factor Research Report

## Dataset Summary

Analysis Timestamp: 2026-06-07 18:46:36.113321
Observation Count: 1658
Date Range: 2017-07-13 00:00:00 -> 2026-06-02 00:00:00

## Executive Summary

Strongest correlation factor: Gift Return (0.592)
Best directional factor: S&P 500 Return (71.35%)
Total factors analysed: 3

## Factor Correlation Matrix

| Factor       | gift_return | vix_return | sp500_return |
|--------------|------------:|-----------:|-------------:|
| gift_return  |       1.000 |     -0.466 |        0.252 |
| vix_return   |      -0.466 |      1.000 |       -0.321 |
| sp500_return |       0.252 |     -0.321 |        1.000 |

## Correlation Ranking (Nifty Gap)

| Rank | Factor         | Correlation |
|------|----------------|------------:|
| 1    | Gift Return    |       0.592 |
| 2    | S&P 500 Return |       0.530 |
| 3    | VIX Return     |      -0.473 |

## Directional Accuracy Ranking (Nifty Gap)

| Rank | Factor         | Accuracy |
|------|----------------|---------:|
| 1    | S&P 500 Return |   71.35% |
| 2    | Gift Return    |   67.67% |
| 3    | VIX Return     |   63.45% |

# Gift Return

## Correlation Analysis

Nifty Gap: 0.592
Sensex Gap: 0.580

## Directional Analysis

Nifty Accuracy: 67.67%
Sensex Accuracy: 65.20%

## Bucket Analysis (Nifty)

| Bucket        | Observations | Accuracy |
|---------------|-------------:|---------:|
| 0.00% - 0.20% |          266 |   53.76% |
| 0.20% - 0.50% |          426 |   60.09% |
| 0.50% - 1.00% |          500 |   71.20% |
| 1.00% - 1.50% |          242 |   74.38% |
| 1.50% - 2.00% |          124 |   80.65% |
| 2.00% - 3.00% |           72 |   83.33% |
| 3.00%+        |           28 |   96.43% |

## Bucket Analysis (Sensex)

| Bucket        | Observations | Accuracy |
|---------------|-------------:|---------:|
| 0.00% - 0.20% |          266 |   51.13% |
| 0.20% - 0.50% |          426 |   58.92% |
| 0.50% - 1.00% |          500 |   68.00% |
| 1.00% - 1.50% |          242 |   71.49% |
| 1.50% - 2.00% |          124 |   79.03% |
| 2.00% - 3.00% |           72 |   79.17% |
| 3.00%+        |           28 |   92.86% |

## Lag Analysis (Nifty)

| Feature           | Correlation |
|-------------------|------------:|
| gift_return       |       0.592 |
| gift_return_lag1  |       0.203 |
| gift_return_lag2  |       0.018 |
| gift_return_lead1 |       0.051 |

## Lag Analysis (Sensex)

| Feature           | Correlation |
|-------------------|------------:|
| gift_return       |       0.580 |
| gift_return_lag1  |       0.193 |
| gift_return_lag2  |       0.004 |
| gift_return_lead1 |       0.047 |

# VIX Return

## Correlation Analysis

Nifty Gap: -0.473
Sensex Gap: -0.460

## Directional Analysis

Nifty Accuracy: 63.45%
Sensex Accuracy: 62.42%

## Bucket Analysis (Nifty)

| Bucket        | Observations | Accuracy |
|---------------|-------------:|---------:|
| 0.00% - 0.20% |           55 |   52.73% |
| 0.20% - 0.50% |          113 |   47.79% |
| 0.50% - 1.00% |          141 |   53.19% |
| 1.00% - 1.50% |          154 |   55.84% |
| 1.50% - 2.00% |          132 |   61.36% |
| 2.00% - 3.00% |          267 |   59.93% |
| 3.00%+        |          796 |   71.23% |

## Bucket Analysis (Sensex)

| Bucket        | Observations | Accuracy |
|---------------|-------------:|---------:|
| 0.00% - 0.20% |           55 |   61.82% |
| 0.20% - 0.50% |          113 |   49.56% |
| 0.50% - 1.00% |          141 |   52.48% |
| 1.00% - 1.50% |          154 |   53.90% |
| 1.50% - 2.00% |          132 |   57.58% |
| 2.00% - 3.00% |          267 |   60.67% |
| 3.00%+        |          796 |   69.10% |

## Lag Analysis (Nifty)

| Feature          | Correlation |
|------------------|------------:|
| vix_return       |      -0.473 |
| vix_return_lag1  |      -0.110 |
| vix_return_lag2  |      -0.045 |
| vix_return_lead1 |      -0.051 |

## Lag Analysis (Sensex)

| Feature          | Correlation |
|------------------|------------:|
| vix_return       |      -0.460 |
| vix_return_lag1  |      -0.104 |
| vix_return_lag2  |      -0.039 |
| vix_return_lead1 |      -0.043 |

# S&P 500 Return

## Correlation Analysis

Nifty Gap: 0.530
Sensex Gap: 0.510

## Directional Analysis

Nifty Accuracy: 71.35%
Sensex Accuracy: 70.69%

## Bucket Analysis (Nifty)

| Bucket        | Observations | Accuracy |
|---------------|-------------:|---------:|
| 0.00% - 0.20% |          342 |   57.60% |
| 0.20% - 0.50% |          387 |   62.27% |
| 0.50% - 1.00% |          435 |   75.40% |
| 1.00% - 1.50% |          228 |   85.09% |
| 1.50% - 2.00% |          113 |   79.65% |
| 2.00% - 3.00% |           99 |   83.84% |
| 3.00%+        |           54 |   92.59% |

## Bucket Analysis (Sensex)

| Bucket        | Observations | Accuracy |
|---------------|-------------:|---------:|
| 0.00% - 0.20% |          342 |   58.19% |
| 0.20% - 0.50% |          387 |   60.47% |
| 0.50% - 1.00% |          435 |   74.71% |
| 1.00% - 1.50% |          228 |   85.09% |
| 1.50% - 2.00% |          113 |   77.88% |
| 2.00% - 3.00% |           99 |   82.83% |
| 3.00%+        |           54 |   92.59% |

## Lag Analysis (Nifty)

| Feature            | Correlation |
|--------------------|------------:|
| sp500_return       |       0.530 |
| sp500_return_lag1  |       0.059 |
| sp500_return_lag2  |       0.100 |
| sp500_return_lead1 |       0.115 |

## Lag Analysis (Sensex)

| Feature            | Correlation |
|--------------------|------------:|
| sp500_return       |       0.510 |
| sp500_return_lag1  |       0.037 |
| sp500_return_lag2  |       0.093 |
| sp500_return_lead1 |       0.112 |

## Research Conclusions

- Strongest correlation factor: Gift Return
- Strongest directional factor: S&P 500 Return
- All factors exhibit signal decay away from the current session.
- Larger factor moves generally produce stronger predictive power.
- Results support further multifactor research.