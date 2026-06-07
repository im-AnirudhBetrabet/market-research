from pathlib  import Path
from datetime import date

from src.ingestion.csv_market_loader    import CsvMarketLoader
from src.ingestion.gift_nifty_loader    import GiftNiftyLoader
from src.ingestion.yfinance_loader      import YahooFinanceLoader
from src.pipelines.market_data_pipeline import MarketDataPipeline
from src.research.dataset_builder       import DatasetBuilder
from src.validators.ohlc_validator      import OHLCValidator

def build_aligned_dataset():
    validator = OHLCValidator()
    print(">> Loading GIFTNIFTY data..")

    gift_pipeline = MarketDataPipeline(loader=GiftNiftyLoader(), validator=validator)
    gift_df, gift_result = gift_pipeline.run(Path("data/raw/gift_nifty.csv"), "gift_nifty")
    csv_pipeline = MarketDataPipeline(loader=CsvMarketLoader(), validator=validator)
    print(">> Loading NIFTY data..")
    nifty_df, nifty_result = csv_pipeline.run("data/raw/nifty.csv", "Nifty")

    print(">> Loading SENSEX data..")
    sensex_df, sensex_result = csv_pipeline.run("data/raw/sensex.csv", "Sensex")

    print(">> Loading INDIAVIX data..")
    vix_df, vix_result = csv_pipeline.run("data/raw/india_vix.csv", "india_vix")

    print(">> Loading S&P500 data..")
    sp500_df, sp500_result = csv_pipeline.run("data/raw/sp500.csv", "sp500")

    aligned_dataset = DatasetBuilder().build(
        gift_dataset=gift_df,
        nifty_dataset=nifty_df,
        sensex_dataset=sensex_df,
        vix_dataset=vix_df,
        sp500_dataset=sp500_df
    )

    df = aligned_dataset.data

    print("\nAligned Dataset Summary")
    print("-"*50)
    print(f"Rows      : {aligned_dataset.row_count}")
    print(f"Start Date: {aligned_dataset.start_date}")
    print(f"End Date  : {aligned_dataset.end_date}")

    print("\nColumns")
    print("-"*50)

    for column in df.columns:
        print(column)

    output_file = Path("data/processed/aligned_dataset.csv")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"\n Saved -> {output_file}")

if __name__ == "__main__":
    build_aligned_dataset()

