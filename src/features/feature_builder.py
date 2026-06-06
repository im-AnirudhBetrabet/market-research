import pandas as pd
from src.domain.models            import FeatureDataset
from src.research.aligned_dataset import AlignedDataset

class FeatureBuilder:
    def build(self, aligned_dataset: AlignedDataset) -> FeatureDataset:
        df = aligned_dataset.data.copy()

        ## Feature
        df["gift_return"]       = df["gift_close"].pct_change()
        df['gift_return_lag1']  = df['gift_return'].shift(1)
        df['gift_return_lag2']  = df['gift_return'].shift(2)
        df['gift_return_lead1'] = df['gift_return'].shift(-1)

        # Target
        df["nifty_previous_close"] = df["nifty_close"].shift(1)
        df["nifty_gap"]            = (df["nifty_open"] - df['nifty_previous_close']) / df['nifty_previous_close']
        df["sensex_prev_close"]    = df["sensex_close"].shift(1)
        df["sensex_gap"]           = (df["sensex_open"] - df["sensex_prev_close"]) / df["sensex_prev_close"]

        df = df.dropna().reset_index(drop=True)

        feature_df = df[[
            'date',
            'gift_return', 'gift_return_lag1', 'gift_return_lag2', 'gift_return_lead1',
            'nifty_gap',
            'sensex_gap'
        ]]

        return FeatureDataset(
            data=feature_df
        )
