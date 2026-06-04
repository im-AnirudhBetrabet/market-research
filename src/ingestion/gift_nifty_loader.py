from pathlib import Path

import pandas as pd


class GiftNiftyLoader:

    def load(self, file_path: Path) -> pd.DataFrame:

        df = pd.read_csv(file_path)

        df = df.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
            }
        )

        # Remove rows with invalid OHLC values
        invalid_mask = (
            (df["open"] == "-")
            | (df["high"] == "-")
            | (df["low"] == "-")
            | (df["close"] == "-")
        )

        invalid_rows = df.loc[invalid_mask]

        if not invalid_rows.empty:
            print(f"Removed {len(invalid_rows)} invalid rows:")

            for row in invalid_rows.itertuples():
                print(f" - {row.date}")

        df = df.loc[~invalid_mask].copy()

        # Convert prices to numeric
        for column in [
            "open",
            "high",
            "low",
            "close",
        ]:
            df[column] = pd.to_numeric(
                df[column]
                .astype(str)
                .str.replace(",", "", regex=False),
                errors="raise",
            )

        # Convert dates
        df["date"] = pd.to_datetime(
            df["date"],
            format="%d %b %Y",
        )

        return df[["date","open","high","low","close"]].sort_values("date").reset_index(drop=True)
