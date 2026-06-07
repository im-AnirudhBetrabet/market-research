from src.domain.models import DirectionalAnalysisResult, FeatureDataset
from src.domain.enums  import RelationshipTypes

class DirectionalAnalysisEngine:

    def calculate(self, dataset: FeatureDataset, feature: str, target: str, relationship: RelationshipTypes) -> DirectionalAnalysisResult:
        feature_direction = dataset.data[feature] > 0
        target_direction  = dataset.data[target] > 0


        if relationship == RelationshipTypes.POSITIVE:
            matches = feature_direction == target_direction
        else:
            matches = feature_direction != target_direction

        total    = len(matches)
        matching = int(matches.sum())
        accuracy = matching / total

        return DirectionalAnalysisResult(
            feature=feature,
            target=target,
            total_observations=total,
            matching_directions=matching,
            accuracy=accuracy,
            relationship=relationship
        )