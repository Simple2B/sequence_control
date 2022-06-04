import pandas as pd


def read_file(file_path: str):
    return pd.read_excel(file_path, sheet_name=None)
