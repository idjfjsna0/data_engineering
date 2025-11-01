# Data Engineering Project
Basic course.

Dataset link: https://drive.google.com/file/d/1sStrkLT-LQ3sIPJD-rPY0LNCCk5l1lbg/view?usp=sharing

The dataset contains data on the spectrum of the transmission coefficient of an interference filter depending on the rotation angle

# Creating env (conda + poetry)
After installing conda, in terminal:
1. conda create -n my_env python=3.13
2. conda activate my_env
3. pip install poetry
4. poetry new trying_de
5. cd trying_de
6. poetry add jupyter pandas matplotlib numpy wget click sqlalchemy dotenv
7. poetry install --no-root

---
## Project structure
```
data_engineering/
├── src/
│   └── etl/                            # Main ETL-pack
│       ├── extract.py                  # Raw dataset downloader (from GD (File ID) or by URL)
│       ├── transform.py                # Dataset cleaner + data type converter
│       ├── load.py                     # Processed data-to-DB uploader (PostgreSQL)
│       └── main.py                     # Combining all stages of the ETL pipeline
│
├── experiments/                        # Experimental scripts, notebooks
│   └── notebooks/
│       ├── EDA+Seaborn/
│       │   └── Seaborned_EDA.ipynb     # EDA with Seaborn visualization
│       └── EDA/
│           └── EDA.ipynb               # EDA
├── pyproject.toml                      # Project dependency settings (Poetry)
│
└── README.md                           # Project description and launch instructions

```
---

## Setting up the environment
1. Clone repo:
   ```bash
   git clone https://github.com/idjfjsna0/data_engineering.git
   cd data_engineering
2. Install dependencies:
   ``` bash
   poetry install
---

## Info about CLI-options
   Calling 'python src/etl/main.py':
   ```bash
   Usage: main.py [OPTIONS] COMMAND [ARGS]...

   ETL pipeline CLI

   Options:
      --help  Show this message and exit.

   Commands:
      extract         Download dataset from GDrive and save as CSV
      load            Load processed CSV into PostgreSQL database
      run-all         Run full ETL pipeline: extract -> transform ->...
      transform-data  Transform raw CSV and save processed CSV
   ```
   Calling 'python src/etl/main.py extract --help':
   ```bash
   Usage: main.py extract [OPTIONS]

      Download dataset from GDrive and save as CSV

   Options:
   --file-id TEXT                  Google Drive file ID or URL
   --show-head / --no-show-head    Show first 10 rows of dataset
   --show-types / --no-show-types  Show column data types of dataset
   --output-dir TEXT               Path to save raw data
   --help                          Show this message and exit.
   ```
   Calling 'python src/etl/main.py transform-data --help':
   ```bash
   Usage: main.py transform-data [OPTIONS]

      Transform raw CSV and save processed CSV

   Options:
      --input-path TEXT  Path to raw CSV
      --output-dir TEXT  Path to save processed data
      --help             Show this message and exit.
   ```
   Calling 'python src/etl/main.py load --help':
   ```bash
   Usage: main.py load [OPTIONS]

      Load processed CSV into PostgreSQL database

   Options:
      --input-path TEXT               Path to processed CSV
      --table-name TEXT               Database table name
      --creds-path TEXT               Path to creds.env
      --visible-password / --invisible-password
                                    Visible DB password in console
      --help                          Show this message and exit.
   ```
## Example calling 'python src/etl/main.py run-all':
   ```bash
   C:\Users\Work\Downloads\data_engineering-main>python src/etl/main.py run-all
   File id: 1sStrkLT-LQ3sIPJD-rPY0LNCCk5l1lbg
   File successfully downloaded.
   Downloaded 2967 rows, 19 columns
   Raw data saved to raw_data\extracted_data.csv
   Processed data saved to processed_data\processed_data.csv
   Skipping database upload (use --to-db to enable).
   ```
## EDA
You can view the notebooks in (requires installed jupyter notebook):
1. data_engineering/experiments/notebooks/EDA/EDA.ipynb
2. data_engineering/experiments/notebooks/EDA+Seaborn/Seaborned_EDA.ipynb