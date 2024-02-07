from io import BytesIO

import hydra
import pandas as pd
import plotly.express as px
import streamlit as st
from helpers import get_s3_client
from omegaconf import DictConfig


def get_data(s3, s3_config):
    # Get the object from S3
    response = s3.get_object(Bucket=s3_config.bucket, Key=s3_config.object_key)

    # Read data from the object's Body directly into a pandas DataFrame
    data = response["Body"].read()
    return pd.read_pickle(BytesIO(data))


def create_streamlit_dashboard(df: pd.DataFrame):
    st.write("# New York Taxi Trips")
    st.write(df)
    st.bar_chart(df, x="passenger_count", y="total_amount")
    st.bar_chart(df, x="pickup_PartofDay", y="passenger_count")
    passenger_count_dist = px.histogram(df, x="passenger_count")
    st.plotly_chart(passenger_count_dist)
    category_order = ["morning", "afternoon", "night", "evening"]
    pickup_partofday_dist = px.histogram(df, x="pickup_PartofDay")
    pickup_partofday_dist.update_layout(
        xaxis={"categoryorder": "array", "categoryarray": category_order}
    )
    st.plotly_chart(pickup_partofday_dist)


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def create_dashboard(config: DictConfig):
    s3 = get_s3_client()
    df = get_data(s3, config.s3.processed)
    create_streamlit_dashboard(df)


if __name__ == "__main__":
    create_dashboard()
