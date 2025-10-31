import pandas as pd

FILE_ID = "1sStrkLT-LQ3sIPJD-rPY0LNCCk5l1lbg"  # ID
file_url = f"https://drive.google.com/uc?id={FILE_ID}"

try:
    raw_data = pd.read_csv(
        file_url, on_bad_lines="skip", skiprows=17, encoding="utf-8", delimiter=";"
    )

    print("File successfully downloaded.")
    print(f"Downloaded {raw_data.shape[0]} rows, {raw_data.shape[1]} columns")

    if raw_data.shape[0] > 0:
        raw_data = raw_data.dropna(how="all")  # Delete all-NaN rows

        for col in raw_data.columns:
            raw_data[col] = pd.to_numeric(raw_data[col], errors="coerce")

        raw_data = raw_data.dropna()  # Delete rows, which contains NaN

        print("\nFirst 10 rows of dataset:")
        print(raw_data.head(10))
        print("Data types of columns:")
        print(raw_data.dtypes)
    else:
        print("No data or wrong format")

except Exception as e:
    print(f"Error: {e}")

raw_data.to_csv("trying_de/spectrum_data.csv", index=False)
