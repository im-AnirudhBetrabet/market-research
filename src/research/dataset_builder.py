import pandas as pd

from src.domain.models            import MarketDataset
from src.research.aligned_dataset import AlignedDataset

class DatasetBuilder:
    def build(self, gift_dataset: MarketDataset, nifty_dataset: MarketDataset, sensex_dataset: MarketDataset, vix_dataset: MarketDataset, sp500_dataset: MarketDataset) -> AlignedDataset:
        gift_df   = self._prepare_dataset(dataset=gift_dataset  , prefix="gift"  )
        nifty_df  = self._prepare_dataset(dataset=nifty_dataset , prefix="nifty" )
        sensex_df = self._prepare_dataset(dataset=sensex_dataset, prefix="sensex")
        vix_df    = self._prepare_dataset(dataset=vix_dataset   , prefix="vix"   )
        sp500_df  = self._prepare_dataset(dataset=sp500_dataset , prefix="sp500" )

        sp500_df["date"] = pd.to_datetime(sp500_df["date"]) + pd.Timedelta(days=1) ## adjusting for difference in trading times.
        common_dates = (set(gift_df['date']) & set(nifty_df['date']) & set(sensex_df['date']) & set(vix_df['date']) & set(sp500_df['date']))

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

        vix_df = self._filter_dates(vix_df, common_dates).drop(
            columns=["index"],
            errors="ignore"
        )

        sp500_df = self._filter_dates(sp500_df, common_dates).drop(
            columns=["index"],
            errors="ignore"
        )

        aligned_df = gift_df.merge(nifty_df, on="date", how="inner").merge(sensex_df, on="date", how="inner").merge(vix_df, on="date", how="inner").merge(sp500_df, on="date", how="inner").sort_values("date").reset_index(drop=True)

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