import pandas as pd

class DataStore:
    def __init__(self):
        self._df: pd.DataFrame | None = None

    def save(self, df: pd.DataFrame) -> None:
        self._df = df

    def get(self) -> pd.DataFrame | None:
        return self._df
    
    def has_data(self) -> bool:
        return self._df is not None
    
store = DataStore()