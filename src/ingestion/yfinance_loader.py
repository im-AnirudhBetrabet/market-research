from datetime import date
import pandas as pd
import yfinance as yf

class YahooFinanceLoader:
    def __init__(self, start_date: date, end_date: date):
        self.start_date = start_date
        self.end_date   = end_date

    def load(self, ticker: str) -> pd.DataFrame:
        df = yf.download(ticker, start=self.start_date, end=self.end_date, auto_adjust=False, progress=False)

        if df.empty:
            raise ValueError(f"No data returned for {ticker}")

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)

        df = df.reset_index().rename(
                columns={
                    "Date" : "date",
                    "Open" : "open",
                    "High" : "high",
                    "Low"  : "low",
                    "Close": "close",
                }
            )



        return df[["date", "open", "high", "low", "close"]].sort_values(by='date').reset_index(drop=True)