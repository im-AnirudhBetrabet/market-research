import pandas as pd

from src.domain.models import ValidationResult
class OHLCValidator:

    REQUIRED_COLUMNS = {
        "date",
        "open",
        "high",
        "low",
        "close",
    }

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        warnings = self._check_for_invalid_rows(df)
        self._validate_columns(df)
        self._validate_empty(df)
        self._validate_duplicates(df)
        self._validate_nulls(df)
        self._validate_numeric_types(df)
        self._validate_positive_prices(df)
        self._validate_sorted_dates(df)
        self._validate_ohlc(df)

        return ValidationResult(
            row_count=len(df),
            duplicate_count=int(
                df["date"].duplicated().sum()
            ),
            null_count=int(
                df.isnull().sum().sum()
            ),
            passed=True,
            warnings=warnings
        )

    def _validate_columns(self, df: pd.DataFrame) -> None:

        missing = self.REQUIRED_COLUMNS - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

    def _validate_empty(self, df: pd.DataFrame ) -> None:

        if df.empty:
            raise ValueError(
                "Dataset is empty"
            )

    def _validate_duplicates(self, df: pd.DataFrame ) -> None:

        duplicates = df["date"].duplicated().sum()

        if duplicates:
            raise ValueError(
                f"Found {duplicates} duplicate dates"
            )

    def _validate_nulls(self, df: pd.DataFrame) -> None:

        nulls = df.isnull().sum().sum()

        if nulls:
            raise ValueError(f"Found {nulls} null values")

    def _validate_numeric_types(self, df: pd.DataFrame) -> None:

        for column in [ "open", "high", "low", "close"]:
            if not pd.api.types.is_numeric_dtype( df[column]):
                raise ValueError(f"{column} is not numeric")

    def _validate_positive_prices(self, df: pd.DataFrame) -> None:

        for column in [ "open", "high", "low", "close"]:
            if (df[column] <= 0).any():
                raise ValueError(
                    f"Non-positive values in {column}"
                )

    def _validate_sorted_dates(self, df: pd.DataFrame,) -> None:
        if not df["date"].is_monotonic_increasing:
            raise ValueError("Dates are not sorted")

    def _validate_ohlc(self, df: pd.DataFrame,) -> None:
        invalid_high = (
            (df["high"] < df["open"])
            |
            (df["high"] < df["close"])
        )

        if invalid_high.any():
            raise ValueError("Invalid high values found")

        invalid_low = (
            (df["low"] > df["open"])
            |
            (df["low"] > df["close"])
        )

        if invalid_low.any():
            raise ValueError("Invalid low values found")

    def _check_for_invalid_rows(self, df):
        warnings = []
        # Remove rows with invalid OHLC values
        invalid_mask = (
                (df["open"] == "-")
                | (df["high"] == "-")
                | (df["low"] == "-")
                | (df["close"] == "-")
        )

        invalid_rows = df.loc[invalid_mask]

        if not invalid_rows.empty:
            warnings.append(f"Removed {len(invalid_rows)} invalid rows:")

            warnings.append(f" - {row.date}" for row in invalid_rows.itertuples())

        df = df.loc[~invalid_mask].copy()

        return warnings