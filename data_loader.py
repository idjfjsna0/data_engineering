import pandas as pd

FILE_ID = "1sStrkLT-LQ3sIPJD-rPY0LNCCk5l1lbg"  # ID
file_url = f"https://drive.google.com/uc?id={FILE_ID}"

try:
    raw_data = pd.read_csv(file_url, on_bad_lines="skip", skiprows=17, encoding="utf-8")

    print("File succesfully downloaded.")
    print(f"Downloaded {raw_data.shape[0]} rows, {raw_data.shape[1]} columns")

    if raw_data.shape[0] > 0:
        print("\nFirst 10 rows of dataset:")
        print(raw_data.head(10))
    else:
        print("No data or wrong format")

except Exception as e:
    print(f"Error: {e}")
