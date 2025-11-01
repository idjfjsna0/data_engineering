import pandas as pd
import os


def extract_data(
    FILE_ID: str, show_head: bool = False, show_types: bool = False
) -> pd.DataFrame:
    """
    Downloading raw dataset from GDrive using FILE_ID and saving it to extracted_data.csv
    """
    if FILE_ID.startswith("http"):
        file_url = FILE_ID
    else:
        file_url = f"https://drive.google.com/uc?id={FILE_ID}"
    try:
        df = pd.read_csv(
            file_url, on_bad_lines="skip", skiprows=17, encoding="utf-8", delimiter=";"
        )

        print("File successfully downloaded.")
        print(f"Downloaded {df.shape[0]} rows, {df.shape[1]} columns")

        if df.shape[0] > 0:
            if show_head:
                print("\nFirst 10 rows of dataset:")
                print(df.head(10))

            if show_types:
                print("Data types of columns:")
                print(df.dtypes)
        else:
            print("No data or wrong format")

    except Exception as e:
        print(f"Error: {e}")
    return df


def save_data_to_csv(df: pd.DataFrame, path: str = "raw_data"):
    os.makedirs(path, exist_ok=True)
    df.to_csv(f"{path}\\extracted_data.csv", index=False)


if __name__ == "__main__":
    FILE_ID = "1sStrkLT-LQ3sIPJD-rPY0LNCCk5l1lbg"
    df = extract_data(FILE_ID)
    save_data_to_csv(df, "raw_data")
