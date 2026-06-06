from pathlib import Path
import matplotlib.pyplot as plt
from src.domain.models import FeatureDataset, BucketAnalysisResult

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

    def build_bucket_chart(self, results: list[BucketAnalysisResult], title: str, output_path: Path) -> None:
        labels   = [result.bucket_name for result in results]
        accuracy = [result.accuracy * 100 for result in results]

        plt.figure(figsize=(10, 6))
        plt.plot(labels, accuracy, marker="o")

        plt.ylabel("Accuracy (%)")
        plt.title(title)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()