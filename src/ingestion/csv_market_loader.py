from pathlib import Path

import pandas as pd


class CsvMarketLoader:

    def load(self, file_path: Path) -> pd.DataFrame:

        df         = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"])

        return df[["date", "open", "high", "low", "close",]].sort_values("date").reset_index(drop=True)