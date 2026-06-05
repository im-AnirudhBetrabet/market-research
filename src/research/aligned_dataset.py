from dataclasses import dataclass
import pandas as pd

@dataclass(slots=True, frozen=True)
class AlignedDataset:
    data: pd.DataFrame

    @property
    def row_count(self):
        return len(self.data)

    @property
    def start_date(self):
        return self.data['date'].min()

    @property
    def end_date(self):
        return self.data['date'].max()