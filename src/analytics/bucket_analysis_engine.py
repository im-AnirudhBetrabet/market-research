from math import inf
import pandas as pd

from src.domain.models import BucketAnalysisResult, FeatureDataset


class BucketAnalysisEngine:
    def __init__(self, buckets: list[float] | None = None):
        self._buckets = buckets if buckets is not None else [0.0, 0.02, 0.05, 0.10, inf]

    def calculate(self, dataset: FeatureDataset, feature: str, target: str) -> list[BucketAnalysisResult]:
        df = dataset.data.copy()

        df['feature_abs'] = df[feature].abs()

        feature_direction = df[feature] > 0
        target_direction  = df[target]  > 0

        df['direction_match'] = feature_direction == target_direction

        results: list[BucketAnalysisResult] = []
        for lower, upper in zip(self._buckets[:-1], self._buckets[1:]):
            bucket_df = df[(df["feature_abs"] >= lower) & (df["feature_abs"] < upper)]

            observations = len(bucket_df)

            if observations == 0:
                continue

            matching = int(bucket_df['direction_match'].sum())

            accuracy = matching / observations

            results.append(
                BucketAnalysisResult(
                    bucket_name=self._format_bucket(lower, upper),
                    lower_bound=lower,
                    upper_bound=upper,
                    observations=observations,
                    matching_directions=matching,
                    accuracy=accuracy
                )
            )
        return results

    @staticmethod
    def _format_bucket(lower: float, upper: float) -> str:
        lower_pct = lower * 100
        if upper == inf:
            return f"{lower_pct:.2f}%+"
        upper_pct = upper * 100

        return f"{lower_pct:.2f}% - {upper_pct:.2f}%"




