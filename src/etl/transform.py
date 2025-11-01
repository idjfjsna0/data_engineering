import pandas as pd
import os


def transform(df: pd.DataFrame, output_dir: str = "processed_data") -> pd.DataFrame:
    """
    Skip all-NaN-rows, data type conversion, export to processed_data.csv
    """
    df = df.dropna(how="all")  # Delete all-NaN rows
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()  # Delete rows, which contains NaN
    os.makedirs("processed_data", exist_ok=True)
    df.to_csv("processed_data/processed_data.csv", index=False)
    return df


if __name__ == "__main__":
    df_raw_path = "raw_data/extracted_data.csv"
    df_raw = pd.read_csv(df_raw_path)
    transform(df_raw)
