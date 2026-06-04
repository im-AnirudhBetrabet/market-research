import pandas as pd
from src.domain.models import MarketDataset, ValidationResult
from pathlib           import Path

class MarketDataPipeline:

    def __init__(self, loader, validator):
        self._loader    = loader
        self._validator = validator

    def run(self, source, dataset_name: str) -> tuple[MarketDataset, ValidationResult]:
        df                = self._loader.load(source)
        validation_result = (self._validator.validate(df))

        dataset = MarketDataset(name=dataset_name, data=df)

        return dataset, validation_result

    def save_data(self, df: pd.DataFrame, name: str) -> None:
        file_path = Path(f"data/raw/{name}.csv")
        df.to_csv(file_path)
        print(f" File saved to {str(file_path)}")
