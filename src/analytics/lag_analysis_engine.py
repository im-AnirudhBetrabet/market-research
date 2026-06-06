from src.domain.models import LagAnalysisResult, FeatureDataset

class LagAnalysisEngine():
    def calculate(self, dataset: FeatureDataset, feature: str, target: str) -> LagAnalysisResult:
        coefficient = dataset.data[feature].corr(dataset.data[target])

        return LagAnalysisResult(
            feature=feature,
            target=target,
            coefficient=float(coefficient)
        )