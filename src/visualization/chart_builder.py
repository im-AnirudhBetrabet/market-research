from pathlib import Path
import matplotlib.pyplot as plt
from src.domain.models import FeatureDataset, BucketAnalysisResult, LagAnalysisResult

class ChartBuilder:
    def build_scatter_plot(self, dataset: FeatureDataset, target: str, output_path: Path) -> None:
        plt.figure(figsize=(10, 6))
        plt.scatter(dataset.data["gift_return"], dataset.data[target])
        plt.xlabel("Gift Return")
        plt.ylabel(target)
        plt.title(f"Gift Return vs {target}")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def build_bucket_accuracy_chart(self, results: list[BucketAnalysisResult], title: str, output_path: Path) -> None:
        labels   = [result.bucket_name for result in results]
        accuracy = [result.accuracy * 100 for result in results]

        plt.figure(figsize=(10, 6))
        plt.plot(labels, accuracy, marker="o")

        plt.ylabel("Accuracy (%)")
        plt.title(title)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def build_lag_analysis_chart(self, results: list[LagAnalysisResult], title: str, output_path: Path) -> None:
        labels = [ result.feature.replace("gift_return_", "").replace("gift_return", "lag0") for result in results]
        values = [ result.coefficient for result in results ]

        plt.figure(figsize=(10, 6))
        plt.bar(labels, values)
        plt.title(title)
        plt.ylabel("Correlation")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def build_bucket_observation_chart(self, results: list[BucketAnalysisResult], title: str, output_path: Path) -> None:
        labels = [ result.bucket_name for result in results ]
        counts = [ result.observations for result in results ]

        plt.figure(figsize=(10, 6))
        plt.bar(labels, counts)
        plt.title(title)
        plt.ylabel("Observations")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def build_correlation_summary_chart(self, nifty_correlation: float, sensex_correlation: float, output_path: Path) -> None:
        labels = ["Nifty Gap", "Sensex Gap"]
        values = [nifty_correlation, sensex_correlation]

        plt.figure(figsize=(8, 6))
        plt.bar(labels, values)
        plt.ylabel("Correlation")
        plt.title("Gift Return Correlation")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()