from dataclasses import dataclass, field
from datetime    import datetime, date
import pandas as pd

from src.domain.enums import RelationshipTypes

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
class   FeatureDataset:
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
    relationship       : RelationshipTypes
    accuracy: float

@dataclass(slots=True, frozen=True)
class BucketAnalysisResult:
    bucket_name: str
    lower_bound: float
    upper_bound: float

    observations       : int
    matching_directions: int
    accuracy           : float

@dataclass(slots=True, frozen=True)
class LagAnalysisResult:
    feature    : str
    target     : str
    coefficient: float

@dataclass(slots=True, frozen=True)
class FactorSummary:
    factor_name: str

    nifty_correlation : CorrelationResult
    sensex_correlation: CorrelationResult

    nifty_directional : DirectionalAnalysisResult
    sensex_directional: DirectionalAnalysisResult

    nifty_buckets : list[BucketAnalysisResult]
    sensex_buckets: list[BucketAnalysisResult]

    nifty_lags : list[LagAnalysisResult]
    sensex_lags: list[LagAnalysisResult]


@dataclass(slots=True, frozen=True)
class FactorRanking:

    factor_name: str

    nifty_correlation : float
    sensex_correlation: float

    nifty_accuracy : float
    sensex_accuracy: float

@dataclass(slots=True, frozen=True)
class FactorCorrelationResult:
    matrix: pd.DataFrame

@dataclass(slots=True, frozen=True)
class CompositeSignalResult:
    signal_name : str
    observations: int
    accuracy    : float
    coverage    : float
    matching_directions: int



@dataclass(slots=True, frozen=True)
class ResearchReport:
    analysis_timestamp: datetime
    observation_count : int
    start_date        : date
    end_date          : date

    factors : list[FactorSummary]
    rankings: list[FactorRanking]

    factor_correlation_matrix: pd.DataFrame
    composite_signals: list[CompositeSignalResult]