import pandas as pd

from src.domain.models            import MarketDataset
from src.research.aligned_dataset import AlignedDataset

class DatasetBuilder:
    def build(self, gift_dataset: MarketDataset, nifty_dataset: MarketDataset, sensex_dataset: MarketDataset) -> AlignedDataset:
        gift_df   = self._prepare_dataset(dataset=gift_dataset  , prefix="gift"  )
        nifty_df  = self._prepare_dataset(dataset=nifty_dataset , prefix="nifty" )
        sensex_df = self._prepare_dataset(dataset=sensex_dataset, prefix="sensex")

        common_dates = (set(gift_df['date']) & set(nifty_df['date']) & set(sensex_df['date']))

        if not common_dates:
            raise ValueError("No common trading dates found")

        gift_df   = self._filter_dates(gift_df, common_dates).drop(
            columns=["index"],
            errors="ignore",
        )
        nifty_df  = self._filter_dates(nifty_df, common_dates).drop(
            columns=["index"],
            errors="ignore",
        )
        sensex_df = self._filter_dates(sensex_df,common_dates).drop(
            columns=["index"],
            errors="ignore",
        )

        aligned_df = gift_df.merge(nifty_df, on="date", how="inner").merge(sensex_df, on="date", how="inner").sort_values("date").reset_index(drop=True)

        return AlignedDataset(
            data=aligned_df
        )

    def _prepare_dataset(self, dataset: MarketDataset, prefix: str) -> pd.DataFrame:
        df = dataset.data.copy()

        return df.rename(columns={
            "close": f"{prefix}_close",
            "high" : f"{prefix}_high",
            "low"  : f"{prefix}_low",
            "open" : f"{prefix}_open"
        })

    def _filter_dates(self, df: pd.DataFrame, common_dates: set) -> pd.DataFrame:
        return df[df['date'].isin(common_dates)].copy().sort_values(by='date').reset_index()