from scripts.ingest_data           import ingest_data
from scripts.build_aligned_dataset import build_aligned_dataset
from src.features.feature_builder  import FeatureBuilder
from pathlib                       import Path
import pandas as pd

from src.research.aligned_dataset import AlignedDataset


def build_features_dataset():
    ingest_data()

    build_aligned_dataset()
    aligned_dataset = AlignedDataset(data=pd.read_csv(Path("data/processed/aligned_dataset.csv")))

    feature_dataset = FeatureBuilder().build(aligned_dataset)

    df = feature_dataset.data

    print("\nFeature Dataset Summary")
    print("-" * 50)

    print(f"Rows: {feature_dataset.row_count}")

    print(df.head(10))

    df.to_csv(
        "data/processed/feature_dataset.csv",
        index=False,
    )

    print(
        aligned_dataset.data[
            [
                "date",
                "gift_close",
                "nifty_open",
                "nifty_close",
            ]
        ].head(5)
    )

    print(
        feature_dataset.data.head(5)
    )

if __name__ == "__main__":
    build_features_dataset()