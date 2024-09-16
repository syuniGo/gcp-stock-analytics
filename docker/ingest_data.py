import sys
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
from scripts.data_repo import DataRepository

def parse_args():
    parser = argparse.ArgumentParser(description='Ingest data to Postgres')
    parser.add_argument('--user', default='root', help='user name for postgres')
    parser.add_argument('--password', default='root', help='password for postgres')
    parser.add_argument('--host', default='pgdatabase', help='host for postgres')
    parser.add_argument('--port', default='5432', help='port for postgres')
    parser.add_argument('--db', default='financial_data', help='database name for postgres')
    parser.add_argument('--table_name', default='financial_data', help='name of the table where we will write the results to')
    parser.add_argument('--data_dir', default='local_data/', help='directory for storing/loading data')
    
    if 'ipykernel' in sys.modules:
        # 我们在 Jupyter 环境中，使用默认值
        return parser.parse_args([])
    else:
        # 我们在常规 Python 环境中，正常解析参数
        return parser.parse_args()

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    data_dir = params.data_dir
    
    # SLOWER workflow settings: full update (the latest data, retrain the model, make inference (few mins)
    FETCH_REPO = False
    
    print('Step 1: Getting data from APIs or Load from disk')
    repo = DataRepository()
    if FETCH_REPO:
        # Fetch All 3 datasets for all dates from APIs
        repo.fetch()
        # save data to a local dir
        repo.persist(data_dir=data_dir)
    else:
        # OR Load from disk
        repo.load(data_dir=data_dir)  

    print('Step 2: Ingesting data into PostgreSQL database')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    # Ingest ticker data
    ingest_dataframe(repo.ticker_df, 'tickers', engine)
    # Ingest indexes data
    ingest_dataframe(repo.indexes_df, 'indexes', engine)
    # Ingest macro data
    ingest_dataframe(repo.macro_df, 'macro', engine)

def ingest_dataframe(df, table_name, engine, chunksize=100000):
    print(f'Ingesting data into {table_name} table')
    
    # Write the DataFrame index as a column
    df = df.reset_index()
    # Create table with correct schema
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    # Ingest data in chunks
    total_rows = len(df)
    for i in range(0, total_rows, chunksize):
        t_start = time()
        chunk = df.iloc[i:i+chunksize]
        chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        t_end = time()
        print(f'Inserted chunk {i//chunksize + 1}, rows {i}-{min(i+chunksize, total_rows)}, took {t_end - t_start:.3f} seconds')
    print(f"Finished ingesting data into the {table_name} table")

if __name__ == '__main__':
    args = parse_args()
    main(args)