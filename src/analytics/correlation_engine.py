from src.domain.models import CorrelationResult, FeatureDataset

class CorrelationEngine:
    def calculate(self, dataset: FeatureDataset, feature: str, target: str) -> CorrelationResult:
        if feature not in dataset.data.columns:
            raise ValueError(f"Feature '{feature}' not found.")

        if target not in dataset.data.columns:
            raise ValueError(f"Target '{target}' not found.")

        coefficient = dataset.data[feature].corr(dataset.data[target])

        return CorrelationResult(
            feature=feature,
            target=target,
            coefficient=float(coefficient)
        )
