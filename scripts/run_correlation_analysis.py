from pathlib import Path

from src.analytics.correlation_engine   import CorrelationEngine
from src.features.feature_builder       import FeatureBuilder
from src.ingestion.csv_market_loader    import CsvMarketLoader
from src.ingestion.gift_nifty_loader    import GiftNiftyLoader
from src.pipelines.market_data_pipeline import MarketDataPipeline
from src.research.dataset_builder       import DatasetBuilder
from src.validators.ohlc_validator      import OHLCValidator

def run_correlation_analysis():
    validator = OHLCValidator()

    gift_pipeline = MarketDataPipeline(loader=GiftNiftyLoader(), validator=validator)
    csv_pipeline  = MarketDataPipeline(loader=CsvMarketLoader(), validator=validator)

    print(">> Loading GIFTNIFTY data..")

    gift_dataset, _ = gift_pipeline.run(source=Path("data/raw/gift_nifty.csv"), dataset_name="gift_nifty",)

    print(">> Loading NIFTY data..")

    nifty_dataset, _ = csv_pipeline.run(source=Path("data/raw/nifty.csv"), dataset_name="nifty")

    print(">> Loading SENSEX data..")

    sensex_dataset, _ = csv_pipeline.run(source=Path("data/raw/sensex.csv"), dataset_name="sensex")

    print(">> Building aligned dataset..")

    aligned_dataset = DatasetBuilder().build(
            gift_dataset=gift_dataset,
            nifty_dataset=nifty_dataset,
            sensex_dataset=sensex_dataset,
        )

    print(">> Building feature dataset..")

    feature_dataset = FeatureBuilder().build(aligned_dataset)

    engine       = CorrelationEngine()
    nifty_result  = engine.calculate(dataset=feature_dataset, feature="gift_return", target="nifty_gap")
    sensex_result = engine.calculate(dataset=feature_dataset, feature="gift_return", target="sensex_gap")

    print("\nCorrelation Analysis")
    print("-" * 60)
    print(
        f"{nifty_result.feature} -> "
        f"{nifty_result.target}: "
        f"{nifty_result.coefficient:.6f}"
    )

    print(
        f"{sensex_result.feature} -> "
        f"{sensex_result.target}: "
        f"{sensex_result.coefficient:.6f}"
    )


if __name__ == "__main__":
    run_correlation_analysis()