# market-research
```
market-research/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── src/
│
│   ├── domain/
│   │   ├── models.py
│   │   └── enums.py
│   │
│   ├── ingestion/
│   │   ├── base.py
│   │   ├── gift_nifty_loader.py
│   │   └── nifty_loader.py
│   │
│   ├── validation/
│   │   ├── base.py
│   │   └── ohlc_validator.py
│   │
│   ├── features/
│   │   ├── gift_features.py
│   │   ├── nifty_features.py
│   │   └── feature_builder.py
│   │
│   ├── analytics/
│   │   ├── correlation_engine.py
│   │   ├── lag_analysis.py
│   │   └── statistics.py
│   │
│   ├── visualization/
│   │   └── plots.py
│   │
│   └── common/
│       ├── constants.py
│       └── exceptions.py
│
├── scripts/
│   ├── validate_data.py
│   ├── build_features.py
│   └── run_correlation.py
│
└── tests/
```