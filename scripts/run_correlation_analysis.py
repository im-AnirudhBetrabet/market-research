from datetime import datetime
from pathlib import Path

from src.analytics.directional_analysis_engine import DirectionalAnalysisEngine
from src.analytics.correlation_engine          import CorrelationEngine
from src.analytics.lag_analysis_engine         import LagAnalysisEngine
from src.features.feature_builder              import FeatureBuilder
from src.ingestion.csv_market_loader           import CsvMarketLoader
from src.ingestion.gift_nifty_loader           import GiftNiftyLoader
from src.pipelines.market_data_pipeline        import MarketDataPipeline
from src.research.dataset_builder              import DatasetBuilder
from src.validators.ohlc_validator             import OHLCValidator
from src.analytics.bucket_analysis_engine      import BucketAnalysisEngine
from src.visualization.chart_builder           import ChartBuilder
from src.reporting.markdown_report_builder     import MarkdownReportBuilder
from src.reporting.factor_ranking_builder      import FactorRankingBuilder
from src.domain.models                         import ResearchReport, FactorSummary
from src.domain.enums                          import RelationshipTypes

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

    print(">> Loading VIX data..")

    vix_dataset, _ = csv_pipeline.run(source=Path("data/raw/india_vix.csv"), dataset_name="vix")

    print(">> Loading S&P 500 data..")

    sp500_dataset, _ = csv_pipeline.run(source=Path("data/raw/sp500.csv"), dataset_name="sp500")

    print(">> Building aligned dataset..")

    aligned_dataset = DatasetBuilder().build(
            gift_dataset=gift_dataset,
            nifty_dataset=nifty_dataset,
            sensex_dataset=sensex_dataset,
            vix_dataset=vix_dataset,
            sp500_dataset=sp500_dataset
        )

    print(">> Building feature dataset..")

    feature_dataset = FeatureBuilder().build(aligned_dataset)

    ## ====== Correlation analysis starts ======
    correlation_engine = CorrelationEngine()
    nifty_gift_correlation  = correlation_engine.calculate(dataset=feature_dataset, feature="gift_return", target="nifty_gap" )
    sensex_gift_correlation = correlation_engine.calculate(dataset=feature_dataset, feature="gift_return", target="sensex_gap")

    nifty_vix_correlation  = correlation_engine.calculate(dataset=feature_dataset, feature="vix_return", target="nifty_gap" )
    sensex_vix_correlation = correlation_engine.calculate(dataset=feature_dataset, feature="vix_return", target="sensex_gap")

    nifty_sp_correlation  = correlation_engine.calculate(dataset=feature_dataset, feature="sp500_return", target="nifty_gap")
    sensex_sp_correlation = correlation_engine.calculate(dataset=feature_dataset, feature="sp500_return", target="sensex_gap")

    ## ====== Correlation analysis ends ======

    ## ====== Directional analysis starts ======
    direction_analysis_engine = DirectionalAnalysisEngine()
    nifty_gift_direction_result  = direction_analysis_engine.calculate(dataset=feature_dataset, feature="gift_return", target="nifty_gap" , relationship=RelationshipTypes.POSITIVE)
    sensex_gift_direction_result = direction_analysis_engine.calculate(dataset=feature_dataset, feature="gift_return", target="sensex_gap", relationship=RelationshipTypes.POSITIVE)

    nifty_vix_direction_result  = direction_analysis_engine.calculate(dataset=feature_dataset, feature="vix_return", target="nifty_gap" , relationship=RelationshipTypes.NEGATIVE)
    sensex_vix_direction_result = direction_analysis_engine.calculate(dataset=feature_dataset, feature="vix_return", target="sensex_gap", relationship=RelationshipTypes.NEGATIVE)

    nifty_sp_direction_result  = direction_analysis_engine.calculate(dataset=feature_dataset, feature="sp500_return", target="nifty_gap", relationship=RelationshipTypes.POSITIVE)
    sensex_sp_direction_result = direction_analysis_engine.calculate(dataset=feature_dataset, feature="sp500_return", target="sensex_gap", relationship=RelationshipTypes.POSITIVE)
    ## ====== Directional analysis ends ======

    ## ====== Bucket analysis starts ======
    bucket_engine = BucketAnalysisEngine(buckets=[0.0, 0.002, 0.005, 0.010, 0.015, 0.020, 0.030, float("inf")])

    nifty_gift_bucket_result  = bucket_engine.calculate(dataset=feature_dataset, feature="gift_return", target="nifty_gap" , relationship=RelationshipTypes.POSITIVE)
    sensex_gift_bucket_result = bucket_engine.calculate(dataset=feature_dataset, feature="gift_return", target="sensex_gap", relationship=RelationshipTypes.POSITIVE)

    nifty_vix_bucket_result   = bucket_engine.calculate(dataset=feature_dataset, feature="vix_return" , target="nifty_gap" , relationship=RelationshipTypes.NEGATIVE)
    sensex_vix_bucket_result  = bucket_engine.calculate(dataset=feature_dataset, feature="vix_return" , target="sensex_gap", relationship=RelationshipTypes.NEGATIVE)

    nifty_sp_bucket_result  = bucket_engine.calculate(dataset=feature_dataset, feature="sp500_return", target="nifty_gap" , relationship=RelationshipTypes.POSITIVE)
    sensex_sp_bucket_result = bucket_engine.calculate(dataset=feature_dataset, feature="sp500_return", target="sensex_gap", relationship=RelationshipTypes.POSITIVE)
    ## ====== Bucket analysis starts ======

    ## ====== Lag analysis starts ======
    lag_engine = LagAnalysisEngine()

    nifty_gift_lag_result = [
        lag_engine.calculate(feature_dataset,"gift_return"      ,"nifty_gap"),
        lag_engine.calculate(feature_dataset,"gift_return_lag1" ,"nifty_gap"),
        lag_engine.calculate(feature_dataset,"gift_return_lag2" ,"nifty_gap"),
        lag_engine.calculate(feature_dataset,"gift_return_lead1","nifty_gap")
    ]

    sensex_gift_lag_result = [
        lag_engine.calculate(feature_dataset, "gift_return"      , "sensex_gap"),
        lag_engine.calculate(feature_dataset, "gift_return_lag1" , "sensex_gap"),
        lag_engine.calculate(feature_dataset, "gift_return_lag2" , "sensex_gap"),
        lag_engine.calculate(feature_dataset, "gift_return_lead1", "sensex_gap")
    ]

    nifty_vix_lag_result = [
        lag_engine.calculate(feature_dataset, "vix_return"      , "nifty_gap"),
        lag_engine.calculate(feature_dataset, "vix_return_lag1" , "nifty_gap"),
        lag_engine.calculate(feature_dataset, "vix_return_lag2" , "nifty_gap"),
        lag_engine.calculate(feature_dataset, "vix_return_lead1", "nifty_gap")
    ]

    sensex_vix_lag_result = [
        lag_engine.calculate(feature_dataset, "vix_return"      , "sensex_gap"),
        lag_engine.calculate(feature_dataset, "vix_return_lag1" , "sensex_gap"),
        lag_engine.calculate(feature_dataset, "vix_return_lag2" , "sensex_gap"),
        lag_engine.calculate(feature_dataset, "vix_return_lead1", "sensex_gap")
    ]

    nifty_sp_lag_result = [
        lag_engine.calculate(feature_dataset, "sp500_return"      , "nifty_gap"),
        lag_engine.calculate(feature_dataset, "sp500_return_lag1" , "nifty_gap"),
        lag_engine.calculate(feature_dataset, "sp500_return_lag2" , "nifty_gap"),
        lag_engine.calculate(feature_dataset, "sp500_return_lead1", "nifty_gap")
    ]

    sensex_sp_lag_result = [
        lag_engine.calculate(feature_dataset, "sp500_return"      , "sensex_gap"),
        lag_engine.calculate(feature_dataset, "sp500_return_lag1" , "sensex_gap"),
        lag_engine.calculate(feature_dataset, "sp500_return_lag2" , "sensex_gap"),
        lag_engine.calculate(feature_dataset, "sp500_return_lead1", "sensex_gap")
    ]
    ## ====== Lag analysis ends ======

    ## ====== Results display starts ======
    print("\nCorrelation Analysis")
    print("-" * 60)
    print(
        f"{nifty_gift_correlation.feature} -> "
        f"{nifty_gift_correlation.target}: "
        f"{nifty_gift_correlation.coefficient:.6f}"
    )

    print(
        f"{sensex_gift_correlation.feature} -> "
        f"{sensex_gift_correlation.target}: "
        f"{sensex_gift_correlation.coefficient:.6f}"
    )

    print(
        f"{nifty_vix_correlation.feature} -> "
        f"{nifty_vix_correlation.target}: "
        f"{nifty_vix_correlation.coefficient:.6f}"
    )

    print(
        f"{sensex_vix_correlation.feature} -> "
        f"{sensex_vix_correlation.target}: "
        f"{sensex_vix_correlation.coefficient:.6f}"
    )

    print(
        f"{nifty_sp_correlation.feature} -> "
        f"{nifty_sp_correlation.target}: "
        f"{nifty_sp_correlation.coefficient:.6f}"
    )

    print(
        f"{sensex_sp_correlation.feature} -> "
        f"{sensex_sp_correlation.target}: "
        f"{sensex_sp_correlation.coefficient:.6f}"
    )

    print("\nDirectional Analysis")
    print("-" * 60)

    print(f"{nifty_gift_direction_result.feature} -> {nifty_gift_direction_result.target}"
        f"\nAccuracy           : {nifty_gift_direction_result.accuracy:.6f}"
        f"\nMatching directions: {nifty_gift_direction_result.matching_directions}"
        f"\nTotal observations : {nifty_gift_direction_result.total_observations}"
    )
    print("\n")
    print(f"{sensex_gift_direction_result.feature} -> {sensex_gift_direction_result.target}"
          f"\nAccuracy           : {sensex_gift_direction_result.accuracy:.6f}"
          f"\nMatching directions: {sensex_gift_direction_result.matching_directions}"
          f"\nTotal observations : {sensex_gift_direction_result.total_observations}"
          )
    print("\n")
    print(f"{nifty_vix_direction_result.feature} -> {nifty_vix_direction_result.target}"
          f"\nAccuracy           : {nifty_vix_direction_result.accuracy:.6f}"
          f"\nMatching directions: {nifty_vix_direction_result.matching_directions}"
          f"\nTotal observations : {nifty_vix_direction_result.total_observations}"
          )
    print("\n")
    print(f"{sensex_vix_direction_result.feature} -> {sensex_vix_direction_result.target}"
          f"\nAccuracy           : {sensex_vix_direction_result.accuracy:.6f}"
          f"\nMatching directions: {sensex_vix_direction_result.matching_directions}"
          f"\nTotal observations : {sensex_vix_direction_result.total_observations}"
          )
    print("\n")
    print(f"{nifty_sp_direction_result.feature} -> {nifty_sp_direction_result.target}"
          f"\nAccuracy           : {nifty_sp_direction_result.accuracy:.6f}"
          f"\nMatching directions: {nifty_sp_direction_result.matching_directions}"
          f"\nTotal observations : {nifty_sp_direction_result.total_observations}"
          )
    print("\n")
    print(f"{sensex_sp_direction_result.feature} -> {sensex_sp_direction_result.target}"
          f"\nAccuracy           : {sensex_sp_direction_result.accuracy:.6f}"
          f"\nMatching directions: {sensex_sp_direction_result.matching_directions}"
          f"\nTotal observations : {sensex_sp_direction_result.total_observations}"
          )

    print("\nBucket Analysis (Gift Return -> Nifty Gap)")
    print("-"*60)

    for result in nifty_gift_bucket_result:
        print(
            f"{result.bucket_name:<20}"
            f" Observations: "
            f"{result.observations:<5}"
            f" Accuracy: "
            f"{result.accuracy:.2%}"
        )

    print("\nBucket Analysis (Gift Return -> Sensex Gap)")
    print("-" * 60)

    for result in sensex_gift_bucket_result:
        print(
            f"{result.bucket_name:<20}"
            f" Observations: "
            f"{result.observations:<5}"
            f" Accuracy: "
            f"{result.accuracy:.2%}"
        )

    print("\nBucket Analysis (VIX Return -> Nifty Gap)")
    print("-" * 60)

    for result in nifty_vix_bucket_result:
        print(
            f"{result.bucket_name:<20}"
            f" Observations: "
            f"{result.observations:<5}"
            f" Accuracy: "
            f"{result.accuracy:.2%}"
        )

    print("\nBucket Analysis (VIX Return -> Sensex Gap)")
    print("-" * 60)

    for result in sensex_vix_bucket_result:
        print(
            f"{result.bucket_name:<20}"
            f" Observations: "
            f"{result.observations:<5}"
            f" Accuracy: "
            f"{result.accuracy:.2%}"
        )

    print("\nBucket Analysis (SP500 Return -> NIFTY Gap)")
    print("-" * 60)

    for result in nifty_sp_bucket_result:
        print(
            f"{result.bucket_name:<20}"
            f" Observations: "
            f"{result.observations:<5}"
            f" Accuracy: "
            f"{result.accuracy:.2%}"
        )

    print("\nBucket Analysis (SP500 Return -> SENSEX Gap)")
    print("-" * 60)

    for result in sensex_sp_bucket_result:
        print(
            f"{result.bucket_name:<20}"
            f" Observations: "
            f"{result.observations:<5}"
            f" Accuracy: "
            f"{result.accuracy:.2%}"
        )

    print("\nLag Analysis")
    print("-" * 60)

    for result in nifty_gift_lag_result:
        print(
            f"{result.feature:<20}"
            f" -> "
            f"{result.target:<15}"
            f": {result.coefficient:.6f}"
        )
    print("\n")
    for result in sensex_gift_lag_result:
        print(
            f"{result.feature:<20}"
            f" -> "
            f"{result.target:<15}"
            f": {result.coefficient:.6f}"
        )
    print("\n")
    for result in nifty_vix_lag_result:
        print(
            f"{result.feature:<20}"
            f" -> "
            f"{result.target:<15}"
            f": {result.coefficient:.6f}"
        )
    print("\n")
    for result in sensex_vix_lag_result:
        print(
            f"{result.feature:<20}"
            f" -> "
            f"{result.target:<15}"
            f": {result.coefficient:.6f}"
        )
    print("\n")
    for result in nifty_sp_lag_result:
        print(
            f"{result.feature:<20}"
            f" -> "
            f"{result.target:<15}"
            f": {result.coefficient:.6f}"
        )
    print("\n")
    for result in sensex_sp_lag_result:
        print(
            f"{result.feature:<20}"
            f" -> "
            f"{result.target:<15}"
            f": {result.coefficient:.6f}"
        )
    ## ====== Results display ends ======

    ## ====== Results visualization starts ======
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

    chart_builder.build_bucket_accuracy_chart(
        results=nifty_gift_bucket_result,
        title=(
            "Gift Return vs "
            "Nifty Gap Accuracy"
        ),
        output_path=Path(
            "charts/nifty_gift_bucket_accuracy.png"
        ),
    )

    chart_builder.build_bucket_accuracy_chart(
        results=sensex_gift_bucket_result,
        title=(
            "Gift Return vs "
            "Sensex Gap Accuracy"
        ),
        output_path=Path(
            "charts/sensex_gift_bucket_accuracy.png"
        ),
    )

    chart_builder.build_bucket_accuracy_chart(
        results=nifty_gift_bucket_result,
        title=(
            "VIX Return vs "
            "Nifty Gap Accuracy"
        ),
        output_path=Path(
            "charts/nifty_vix_bucket_accuracy.png"
        ),
    )

    chart_builder.build_bucket_accuracy_chart(
        results=sensex_vix_bucket_result,
        title=(
            "VIX Return vs "
            "Sensex Gap Accuracy"
        ),
        output_path=Path(
            "charts/sensex_vix_bucket_accuracy.png"
        ),
    )

    chart_builder.build_bucket_accuracy_chart(
        results=nifty_sp_bucket_result,
        title=(
            "S&P 500 Return vs "
            "Nifty Gap Accuracy"
        ),
        output_path=Path(
            "charts/nifty_sp_bucket_accuracy.png"
        ),
    )

    chart_builder.build_bucket_accuracy_chart(
        results=sensex_sp_bucket_result,
        title=(
            "SP Return vs "
            "Sensex Gap Accuracy"
        ),
        output_path=Path(
            "charts/sensex_sp_bucket_accuracy.png"
        ),
    )

    chart_builder.build_bucket_observation_chart(
        results=nifty_gift_bucket_result,
        title="Gift Return vs Nifty gap observations",
        output_path=Path("charts/nifty_gift_bucket_counts.png")
    )

    chart_builder.build_bucket_observation_chart(
        results=sensex_gift_bucket_result,
        title="Gift Return vs Sensex gap observations",
        output_path=Path("charts/sensex_gift_bucket_counts.png")
    )

    chart_builder.build_bucket_observation_chart(
        results=nifty_vix_bucket_result,
        title="VIX Return vs Nifty gap observations",
        output_path=Path("charts/nifty_vix_bucket_counts.png")
    )

    chart_builder.build_bucket_observation_chart(
        results=sensex_vix_bucket_result,
        title="VIX Return vs Sensex gap observations",
        output_path=Path("charts/sensex_vix_bucket_counts.png")
    )

    chart_builder.build_bucket_observation_chart(
        results=nifty_sp_bucket_result,
        title="S&P 500 Return vs Nifty gap observations",
        output_path=Path("charts/nifty_sp_bucket_counts.png")
    )

    chart_builder.build_bucket_observation_chart(
        results=sensex_sp_bucket_result,
        title="S&P 500 Return vs Sensex gap observations",
        output_path=Path("charts/sensex_sp_bucket_counts.png")
    )

    chart_builder.build_lag_analysis_chart(
        results=nifty_gift_lag_result,
        title="GIFT return vs Nifty gap signal strength analysis",
        output_path=Path("charts/nifty_gift_lag_analysis.png")
    )

    chart_builder.build_lag_analysis_chart(
        results=sensex_gift_lag_result,
        title="GIFT return vs Sensex gap signal strength analysis",
        output_path=Path("charts/sensex_gift_lag_analysis.png")
    )

    chart_builder.build_lag_analysis_chart(
        results=nifty_vix_lag_result,
        title="VIX return vs Nifty gap signal strength analysis",
        output_path=Path("charts/nifty_vix_lag_analysis.png")
    )

    chart_builder.build_lag_analysis_chart(
        results=sensex_vix_lag_result,
        title="VIX return vs Sensex gap signal strength analysis",
        output_path=Path("charts/sensex_vix_lag_analysis.png")
    )

    chart_builder.build_lag_analysis_chart(
        results=nifty_sp_lag_result,
        title="S&P 500 return vs Nifty gap signal strength analysis",
        output_path=Path("charts/nifty_sp_lag_analysis.png")
    )

    chart_builder.build_lag_analysis_chart(
        results=sensex_sp_lag_result,
        title="S&P 500 return vs Sensex gap signal strength analysis",
        output_path=Path("charts/sensex_sp_lag_analysis.png")
    )

    chart_builder.build_correlation_summary_chart(
        nifty_correlation=nifty_gift_correlation.coefficient,
        sensex_correlation=sensex_gift_correlation.coefficient,
        output_path=Path("charts/gift_correlation_summary.png"),
        feature="gift"
    )

    chart_builder.build_correlation_summary_chart(
        nifty_correlation=nifty_vix_correlation.coefficient,
        sensex_correlation=sensex_vix_correlation.coefficient,
        output_path=Path("charts/vix_correlation_summary.png"),
        feature="vix"
    )

    chart_builder.build_correlation_summary_chart(
        nifty_correlation=nifty_sp_correlation.coefficient,
        sensex_correlation=sensex_sp_correlation.coefficient,
        output_path=Path("charts/sp_correlation_summary.png"),
        feature="vix"
    )

    gift_factor = FactorSummary(
        factor_name="Gift Return",

        nifty_correlation=nifty_gift_correlation,
        sensex_correlation=sensex_gift_correlation,

        nifty_directional=nifty_gift_direction_result,
        sensex_directional=sensex_gift_direction_result,

        nifty_buckets=nifty_gift_bucket_result,
        sensex_buckets=sensex_gift_bucket_result,

        nifty_lags=nifty_gift_lag_result,
        sensex_lags=sensex_gift_lag_result,
    )

    vix_factor = FactorSummary(
        factor_name="VIX Return",

        nifty_correlation=nifty_vix_correlation,
        sensex_correlation=sensex_vix_correlation,

        nifty_directional=nifty_vix_direction_result,
        sensex_directional=sensex_vix_direction_result,

        nifty_buckets=nifty_vix_bucket_result,
        sensex_buckets=sensex_vix_bucket_result,

        nifty_lags=nifty_vix_lag_result,
        sensex_lags=sensex_vix_lag_result,
    )

    sp_factor = FactorSummary(
        factor_name="S&P 500 Return",

        nifty_correlation=nifty_sp_correlation,
        sensex_correlation=sensex_sp_correlation,

        nifty_directional=nifty_sp_direction_result,
        sensex_directional=sensex_sp_direction_result,

        nifty_buckets=nifty_sp_bucket_result,
        sensex_buckets=sensex_sp_bucket_result,

        nifty_lags=nifty_sp_lag_result,
        sensex_lags=sensex_sp_lag_result,
    )
    factor_rankings_builder = FactorRankingBuilder()
    factor_rankings =  factor_rankings_builder.build([
            gift_factor,
            vix_factor,
            sp_factor
        ])
    report = ResearchReport(
        analysis_timestamp=datetime.now(),
        observation_count=len(
            feature_dataset.data
        ),
        start_date=feature_dataset.data[
            "date"
        ].min(),
        end_date=feature_dataset.data[
            "date"
        ].max(),
        factors=[
            gift_factor,
            vix_factor,
            sp_factor
        ],
        rankings=factor_rankings
    )

    chart_builder.build_factor_ranking_chart(
        factors=report.factors,
        target="nifty",
        output_path=Path(
            "charts/factor_ranking_nifty.png"
        ),
    )

    chart_builder.build_factor_ranking_chart(
        factors=report.factors,
        target="sensex",
        output_path=Path(
            "charts/factor_ranking_sensex.png"
        ),
    )

    ## ====== Results visualization ends ======

    ## ====== Reporting starts ======
    MarkdownReportBuilder().build(
        report=report,
        output_file=Path(
            "reports/research_report.md"
        ),
    )
    ## ====== Reporting ends ======
if __name__ == "__main__":
    run_correlation_analysis()