from pathlib                            import Path
from datetime                           import date
from src.ingestion.gift_nifty_loader    import GiftNiftyLoader
from src.ingestion.yfinance_loader      import YahooFinanceLoader
from src.pipelines.market_data_pipeline import MarketDataPipeline
from src.validators.ohlc_validator      import OHLCValidator

def print_result( dataset_name: str, result) -> None:
    print(f"\n{dataset_name}")
    print("-" * 40)
    print(result)


def ingest_data():
    validator = OHLCValidator()

    gift_pipeline        = MarketDataPipeline(loader=GiftNiftyLoader(), validator=validator)
    gift_df, gift_result = gift_pipeline.run(Path("data/raw/gift_nifty.csv"), "gift_nifty")
    print_result("Gift Nifty",gift_result)

    yahoo_loader           = YahooFinanceLoader(date(2015, 1, 1), date.today())
    nifty_pipeline         = MarketDataPipeline(loader=yahoo_loader, validator=validator)
    nifty_df, nifty_result = nifty_pipeline.run("^NSEI", "Nifty")
    nifty_pipeline.save_data(nifty_df.data, "nifty")

    sensex_pipeline          = MarketDataPipeline(loader=yahoo_loader, validator=validator)
    sensex_df, sensex_result = nifty_pipeline.run("^BSESN", "Sensex")
    sensex_pipeline.save_data(sensex_df.data, "sensex")
    print_result("Nifty", nifty_result)

    print_result("Sensex", sensex_result)

    vix_pipeline = MarketDataPipeline(loader=yahoo_loader, validator=validator)
    vix_df, vix_result = vix_pipeline.run("^INDIAVIX", "VIX")
    vix_pipeline.save_data(vix_df.data, "india_vix")

    print_result("VIX", vix_result)

if __name__ == "__main__":
    ingest_data()