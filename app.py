import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

from src.data_loader import get_asteroid_data
from src.data_processor import process_asteroid_data
from src.data_visualizer import (
    plot_approaches_over_time,
    plot_risk_scatter,
    plot_diameter_distribution,
    plot_hazardous_counts,
    plot_velocity_box
)

st.set_page_config(
    page_title="Astro-Intelligence",
    layout="wide"
)

st.title("Asteroid Risk Intelligence Dashboard")
st.write(
    "Analyze near-Earth objects using NASA's Near Earth Object Web Service data. "
    "Explore asteroid risk based on size, speed, and proximity."
)

st.sidebar.header("Filters")

default_end = datetime.today()
default_start = default_end - timedelta(days=7)

start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", default_end)

start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

if start_date > end_date:
    st.error("Start date must be before end date")
    st.stop()

if (end_date - start_date).days > 30:
    st.warning("Please select a range under 30 days")
    st.stop()

# Load data

@st.cache_data
def load_data(start_date, end_date):
    raw_data = get_asteroid_data(start_date, end_date)
    df = process_asteroid_data(raw_data)
    return df

with st.spinner("Fetching asteroid data..."):
    df = load_data(start_date, end_date)

# Metrics

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Asteroids", len(df))
col2.metric("Hazardous Asteroids", df["is_hazardous"].sum())
col3.metric(
    "Avg Velocity (km/s)",
    round(df["velocity_km_s"].mean(), 2)
)

#Graphs

st.subheader("Asteroid Activity Over Time")
st.write("Tracks how many asteroids approach Earth each day.")
st.plotly_chart(plot_approaches_over_time(df), use_container_width=True)

st.subheader("Risk Distribution")
st.write("Shows relationship between distance, velocity, and size. ")
st.plotly_chart(plot_risk_scatter(df), use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Size Distribution")
    st.plotly_chart(plot_diameter_distribution(df), use_container_width=True)

with col2:
    st.subheader("Hazardous vs Non-Hazardous")
    st.plotly_chart(plot_hazardous_counts(df), use_container_width=True)

st.subheader("Velocity by Hazard Level")
st.write("Compares how fast hazardous vs non-hazardous asteroids travel.")
st.plotly_chart(plot_velocity_box(df), use_container_width=True)