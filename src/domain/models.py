from dataclasses import dataclass, field
from datetime    import datetime
import pandas as pd

@dataclass(frozen=True)
class MarketBar:
    timestamp: datetime
    open     : float
    high     : float
    low      : float
    close    : float

@dataclass
class ValidationResult:
    duplicate_count: int
    null_count     : int
    row_count      : int
    passed         : int
    warnings       : list[str] = field(
        default_factory=list
    )

@dataclass(slots=True, frozen=True)
class MarketDataset:
    name: str
    data: pd.DataFrame

@dataclass(slots=True, frozen=True)
class FeatureDataset:
    data: pd.DataFrame

    @property
    def row_count(self) -> int:
        return len(self.data)

@dataclass(slots=True, frozen=True)
class CorrelationResult:
    feature    : str
    target     : str
    coefficient: float

@dataclass(slots=True, frozen=True)
class DirectionalAnalysisResult:
    feature: str
    target : str

    total_observations : int
    matching_directions: int

    accuracy: float