from sqlalchemy import create_engine, text, inspect
import pandas as pd
import os
from dotenv import load_dotenv


def write_data_to_db(
    df: pd.DataFrame,
    table_name: str = "alexey",
    creds_path: str = "db_auth/auth.env",
    visible_password: bool = True,
):
    """
    Connecting to database and write first 100 raws of dataset there
    """

    load_dotenv(creds_path)  # loading auth data

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_url = os.getenv("DB_URL")
    db_port = os.getenv("DB_PORT")
    db_name = "homeworks"

    print("Authorization parameters:")
    print(f"Username {db_user};\n")
    if visible_password:
        print(f"Password: {db_password};")
    else:
        print(f"Password: {'*'*len(db_password)};")
        print(f"URL: {db_url};\n" f"Port: {db_port};\n" f"Name: {db_name}.\n")

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_url}:{db_port}/{db_name}"
    )  # creating engine - database connecting object

    with engine.connect() as conn:
        print("Connnection success.")  # print if connection attempt is succesful

    df.to_sql(
        name=table_name,
        con=engine,
        schema="public",
        if_exists="replace",
        index=True,  # saves DataFrame index as column
    )
    print("Data was written successfully.")

    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE public.alexey ADD PRIMARY KEY (index)"))


def show_table_structure():
    """
    Prints database table column names and types
    """
    inspector = inspect(engine)
    columns = inspector.get_columns("alexey", schema="public")

    print("\nTable structure:")
    print({col["name"]: col["type"] for col in columns})
