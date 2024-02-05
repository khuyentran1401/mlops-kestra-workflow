from datetime import datetime

import hydra
import pandas as pd
from omegaconf import DictConfig


def get_data(file_path: str, datetime_columns: list):
    print(f"Get data from {file_path}")
    df = pd.read_csv(file_path, parse_dates=datetime_columns)
    return df


def get_part_of_day(hour: int):
    # Convert hour to datetime object
    datetime_object = datetime.fromtimestamp(hour * 3600)

    # Get the time of day based on the hour
    if datetime_object.hour < 12:
        return "morning"
    elif datetime_object.hour < 17:
        return "afternoon"
    elif datetime_object.hour < 20:
        return "evening"
    else:
        return "night"


def extract_date_features(df: pd.DataFrame, datetime_column: str):
    print(f"Extract date features from {datetime_column}")
    prefix = datetime_column.split("_")[0]
    df[f"{prefix}_DayofMonth"] = df[datetime_column].dt.day
    df[f"{prefix}_Hour"] = df[datetime_column].dt.hour
    df[f"{prefix}_PartofDay"] = df[f"{prefix}_Hour"].apply(get_part_of_day)
    df[f"{prefix}_DayofWeek"] = df[datetime_column].dt.dayofweek
    return df


def save_df(df: pd.DataFrame, filename: str):
    print(f"Save data to {filename}")
    df.to_pickle(filename)
    return df


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def process_data(config: DictConfig):
    datetime_columns = list(config.columns.datetime)
    df = get_data(config.data.raw, datetime_columns=datetime_columns)
    for column in datetime_columns:
        df = extract_date_features(df, datetime_column=column)
    save_df(df, config.data.processed)


if __name__ == "__main__":
    process_data()
