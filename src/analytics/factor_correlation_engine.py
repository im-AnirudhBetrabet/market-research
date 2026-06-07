from src.domain.models import FactorCorrelationResult, FeatureDataset


class FactorCorrelationEngine:

    def calculate(self,dataset: FeatureDataset,features: list[str]) -> FactorCorrelationResult:
        correlation_matrix = dataset.data[features].corr()
        return FactorCorrelationResult(
            matrix=correlation_matrix
        )