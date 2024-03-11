import os
from pathlib import Path

import boto3
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def load_data(path: str, csv_delimeter=","):
    """Load data from path"""
    file_path = Path(path)
    if file_path.suffix == ".csv":
        df = pd.read_csv(file_path, delimiter=csv_delimeter)
    elif file_path.suffix == ".pkl":
        df = pd.read_pickle(file_path)
    else:
        raise ValueError("File format not supported. Please use a CSV or PKL file.")

    return df


def save_data(df: pd.DataFrame, path: str):
    """Save data to path"""
    Path(path).parent.mkdir(exist_ok=True)
    df.to_pickle(path)


def get_s3_client():
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY_ID")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return s3
