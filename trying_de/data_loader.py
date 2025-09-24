import pandas as pd

file_id = "1sStrkLT-LQ3sIPJD-rPY0LNCCk5l1lbg"  # ID файла на Google Drive
file_url = f"https://drive.google.com/uc?id={file_id}"

raw_data = pd.read_csv(file_url, skiprows=18, delimiter=";", encoding="utf-8")
print(raw_data[0])
raw_data.head(10)  # выводим на экран первые 10 строк для проверки
# https://drive.google.com/file/d/1sStrkLT-LQ3sIPJD-rPY0LNCCk5l1lbg/view?usp=sharing
