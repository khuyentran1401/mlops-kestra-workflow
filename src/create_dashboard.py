import hydra
import pandas as pd
import plotly.express as px
import streamlit as st
from omegaconf import DictConfig


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def create_dashboard(config: DictConfig):
    st.write("# New York Taxi Trips")
    df = pd.read_pickle(config.data.processed)
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


if __name__ == "__main__":
    create_dashboard()
