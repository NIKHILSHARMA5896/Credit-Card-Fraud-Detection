import numpy as np
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)
import os
from sklearn.model_selection import train_test_split
import yaml
import sys
from src.logger import logging
from src.connections import s3_connection
from dotenv import load_dotenv
load_dotenv(override=True)

def load_data(data_url: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(data_url)
        logging.info('Data loaded from %s', data_url)
        return df
    except pd.errors.ParserError as e:
        logging.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error occurred while loading the data: %s', e)
        raise

def save_data(df: pd.DataFrame, data_path: str) -> None:
    """Save the dataset."""
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        df.to_csv(os.path.join(raw_data_path, "data.csv"), index=False)
        logging.info('Data saved to %s', raw_data_path)
    except Exception as e:
        logging.error('Unexpected error occurred while saving the data: %s', e)
        raise

def main():
    try:
        bucket_name = os.getenv("BUCKET_NAME")
        aws_access_key = os.getenv("AWS_ACCESS_KEY")
        aws_secret_key = os.getenv("AWS_SECRET_KEY")
        FILE_KEY = "creditcard.csv"  # Path inside S3 bucket
        
        s3 = s3_connection.s3_operations(bucket_name, aws_access_key, aws_secret_key)
        df = s3.fetch_file_from_s3(FILE_KEY)

        ##df = load_data(data_url="https://raw.githubusercontent.com/vikashishere/Datasets/refs/heads/main/creditcard.csv")

        if df is None:
            logging.error("Data fetching failed, received None. Exiting.")
            return
        
        save_data(df, data_path='./data')
    except Exception as e:
        logging.error('Failed to complete the data ingestion process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
