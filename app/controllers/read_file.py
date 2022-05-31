import pandas as pd

# from app.config import settings


def read_file(file_path: str):
    return pd.read_excel(file_path, sheet_name=None)
