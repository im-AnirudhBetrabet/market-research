from pathlib import Path

from src.analytics.directional_analysis_engine import DirectionalAnalysisEngine
from src.analytics.correlation_engine          import CorrelationEngine
from src.features.feature_builder              import FeatureBuilder
from src.ingestion.csv_market_loader           import CsvMarketLoader
from src.ingestion.gift_nifty_loader           import GiftNiftyLoader
from src.pipelines.market_data_pipeline        import MarketDataPipeline
from src.research.dataset_builder              import DatasetBuilder
from src.validators.ohlc_validator             import OHLCValidator
from src.analytics.bucket_analysis_engine      import BucketAnalysisEngine
from src.visualization.chart_builder           import ChartBuilder

def run_correlation_analysis():
    validator = OHLCValidator()


    charts_dir    = Path("charts")
    charts_dir.mkdir(parents=True, exist_ok=True)
    chart_builder = ChartBuilder()

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

    correlation_engine = CorrelationEngine()
    nifty_result       = correlation_engine.calculate(dataset=feature_dataset, feature="gift_return", target="nifty_gap")
    sensex_result      = correlation_engine.calculate(dataset=feature_dataset, feature="gift_return", target="sensex_gap")

    direction_analysis_engine = DirectionalAnalysisEngine()
    nifty_direction_result    = direction_analysis_engine.calculate(dataset=feature_dataset, feature="gift_return", target="nifty_gap")
    sensex_direction_result   = direction_analysis_engine.calculate(dataset=feature_dataset, feature="gift_return", target="sensex_gap")

    bucket_engine = BucketAnalysisEngine(buckets=[0.0, 0.002, 0.005, 0.010, 0.015, 0.020, 0.030, float("inf")])

    nifty_bucket_result  = bucket_engine.calculate(dataset=feature_dataset, feature="gift_return", target="nifty_gap")
    sensex_bucket_result = bucket_engine.calculate(dataset=feature_dataset, feature="gift_return", target="sensex_gap")

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

    print("\nDirectional Analysis")
    print("-" * 60)
    print(f"{nifty_direction_result.feature} -> {nifty_direction_result.target}"
        f"\nAccuracy           : {nifty_direction_result.accuracy:.6f}"
        f"\nMatching directions: {nifty_direction_result.matching_directions}"
        f"\nTotal observations : {nifty_direction_result.total_observations}"
    )

    print(f"{sensex_direction_result.feature} -> {sensex_direction_result.target}"
          f"\nAccuracy           : {sensex_direction_result.accuracy:.6f}"
          f"\nMatching directions: {sensex_direction_result.matching_directions}"
          f"\nTotal observations : {sensex_direction_result.total_observations}"
          )

    print("\nBucket Analysis (Gift Return -> Nifty Gap)")
    print("-"*60)

    for result in nifty_bucket_result:
        print(
            f"{result.bucket_name:<20}"
            f" Observations: "
            f"{result.observations:<5}"
            f" Accuracy: "
            f"{result.accuracy:.2%}"
        )

    print("\nBucket Analysis (Gift Return -> Sensex Gap)")
    print("-" * 60)

    for result in sensex_bucket_result:
        print(
            f"{result.bucket_name:<20}"
            f" Observations: "
            f"{result.observations:<5}"
            f" Accuracy: "
            f"{result.accuracy:.2%}"
        )

        chart_builder.build_scatter_plot(
            dataset=feature_dataset,
            target="nifty_gap",
            output_path=Path("charts/nifty_scatter.png")
        )
        chart_builder.build_scatter_plot(
            dataset=feature_dataset,
            target="sensex_gap",
                output_path=Path("charts/sensex_scatter.png")
        )

        chart_builder.build_bucket_chart(
            results=nifty_bucket_result,
            title=(
                "Gift Return vs "
                "Nifty Gap Accuracy"
            ),
            output_path=Path(
                "charts/nifty_bucket_accuracy.png"
            ),
        )

        chart_builder.build_bucket_chart(
            results=sensex_bucket_result,
            title=(
                "Gift Return vs "
                "Sensex Gap Accuracy"
            ),
            output_path=Path(
                "charts/sensex_bucket_accuracy.png"
            ),
        )

if __name__ == "__main__":
    run_correlation_analysis()