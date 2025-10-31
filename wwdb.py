from sqlalchemy import create_engine, text, inspect
import pandas as pd
import os
from dotenv import load_dotenv



def data_load():
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

            raw_data = raw_data.head(100)
        else:
            print("No data or wrong format")

    except Exception as e:
        print(f"Error: {e}")
    return raw_data


def write_data_to_db(df, table_name):
    df.to_sql(
        name=table_name, con=engine, schema="public", if_exists="replace", index=True
    )


if __name__ == "__main__":
    load_dotenv(r"C:\Users\U53R\DE2025\data_engineering\database\auth.env")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_url = os.getenv("DB_URL")
    db_port = os.getenv("DB_PORT")
    db_name = "homeworks"
    table_name = "alexey"
    print(db_user, db_password, db_url, db_port, db_name)

    df = data_load()
    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_url}:{db_port}/{db_name}"
    )
    with engine.connect() as conn:
        print("Connnection success.")
    write_data_to_db(df, table_name)
    print("Data was written successfully.")
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE public.alexey ADD PRIMARY KEY (index)"))

    inspector = inspect(engine)
    columns = inspector.get_columns("alexey", schema="public")

    print("\nTable structure:")
    print({col["name"]: col["type"] for col in columns})
