import click
import pandas as pd
from extract import extract_data, save_data_to_csv
from transform import transform
from load import write_data_to_db


@click.group()  # group a few commands in 1 func
def cli():  # parent group of commands
    """ETL pipeline CLI"""
    pass


# ---------------- Extract ----------------
@cli.command()  # turns func into CLI-command
@click.option("--file-id", prompt=True, help="Google Drive file ID or URL")
@click.option(
    "--show-head/--no-show-head",
    default=False,
    type=bool,
    help="Show first 10 rows of dataset",
)
@click.option(
    "--show-types/--no-show-types",
    default=False,
    type=bool,
    help="Show column data types of dataset",
)
@click.option("--output-dir", default="raw_data", help="Path to save raw data")
def extract(file_id, show_head, show_types, output_dir):
    """Download dataset from GDrive and save as CSV"""
    df = extract_data(FILE_ID=file_id, show_head=show_head, show_types=show_types)
    save_data_to_csv(df, output_dir)
    click.echo(f"Raw data saved to {output_dir}\\extracted_data.csv")


# ---------------- Transform ----------------
@cli.command()
@click.option(
    "--input-path", default="raw_data/extracted_data.csv", help="Path to raw CSV"
)
@click.option(
    "--output-dir", default="processed_data", help="Path to save processed data"
)
def transform_data(input_path, output_dir):
    """Transform raw CSV and save processed CSV"""
    df = pd.read_csv(input_path)
    df_transformed = transform(df, output_dir)
    click.echo(f"Processed data saved to {output_dir}\\processed_data.csv")


# ---------------- Load ----------------
@cli.command()
@click.option(
    "--input-path",
    default="processed_data/processed_data.csv",
    help="Path to processed CSV",
)
@click.option("--table-name", default="alexey", help="Database table name")
@click.option("--creds-path", default="db_auth/auth.env", help="Path to creds.env")
@click.option(
    "--visible-password/--invisible-password",
    default=False,
    type=bool,
    help="Visible DB password in console",
)
def load(input_path, table_name, creds_path, show_password):
    """Load processed CSV into PostgreSQL database"""
    df = pd.read_csv(input_path)
    write_data_to_db(
        df, table_name=table_name, creds_path=creds_path, visible_password=show_password
    )
    click.echo(f"Data loaded into table '{table_name}' successfully!")


# ---------------- Run All ----------------
@cli.command()
@click.option("--file-id", prompt=True, help="Google Drive file ID")
@click.option(
    "--show-head/--no-show-head", default=False, type=bool, help="Show first 10 rows"
)
@click.option(
    "--show-types/--no-show-types",
    default=False,
    type=bool,
    help="Show column data types",
)
@click.option("--raw-dir", default="raw_data", help="Directory for raw data")
@click.option(
    "--processed-dir", default="processed_data", help="Directory for processed data"
)
@click.option("--to-db", is_flag=True, help="Upload processed data to database")
@click.option("--table-name", default="alexey", help="Database table name")
@click.option(
    "--creds-path", default="db_auth/auth.env", help="Path to .env with DB credentials"
)
@click.option(
    "--visible-password/--invisible-password",
    default=False,
    type=bool,
    help="Show DB password in console",
)
def run_all(
    file_id,
    show_head,
    show_types,
    raw_dir,
    processed_dir,
    to_db,
    table_name,
    creds_path,
    visible_password,
):
    """Run full ETL pipeline: extract -> transform -> (optional) load"""

    # Extract
    df_raw = extract_data(FILE_ID=file_id, show_head=show_head, show_types=show_types)
    save_data_to_csv(df_raw, raw_dir)
    click.echo(f"Raw data saved to {raw_dir}\\extracted_data.csv")

    # Transform
    df_transformed = transform(df_raw, processed_dir)
    click.echo(f"Processed data saved to {processed_dir}\\processed_data.csv")

    # Load (опционально)
    if to_db:
        write_data_to_db(
            df_transformed,
            table_name=table_name,
            creds_path=creds_path,
            visible_password=visible_password,
        )
        click.echo(f"Data loaded into table '{table_name}' successfully!")
    else:
        click.echo("Skipping database upload (use --to-db to enable).")


if __name__ == "__main__":
    cli()
