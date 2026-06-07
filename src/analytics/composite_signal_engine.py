from src.domain.models import CompositeSignalResult, FeatureDataset


class CompositeSignalEngine:
    def calculate(self, dataset: FeatureDataset, signal_name: str, condition, target_column: str, expected_direction: bool) -> CompositeSignalResult:

        df = dataset.data.copy()

        signal_df    = df[condition(df)]
        observations = len(signal_df)

        total_observations = len(df)
        if observations == 0:
            return CompositeSignalResult(
                signal_name=signal_name,
                observations=0,
                matching_directions=0,
                accuracy=0.0,
            )

        target_direction = signal_df[target_column] > 0
        matches          = target_direction == expected_direction

        matching_directions = int(matches.sum())
        accuracy            = matching_directions / observations
        coverage            = observations / total_observations
        return CompositeSignalResult(
            signal_name=signal_name,
            observations=observations,
            matching_directions=matching_directions,
            accuracy=accuracy,
            coverage=coverage
        )