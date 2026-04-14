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
    plot_velocity_box,
    plot_top_risk_asteroids
)

st.set_page_config(
    page_title="Astro-Intelligence",
    layout="wide"
)

st.title("Asteroid Risk Intelligence Dashboard")
st.write(
    "Analyze near-Earth objects using NASA's Near Earth Object Web Service data. "
    "Explore asteroid risk based on size, velocity, and proximity."
)

# Sidebar Filters
st.sidebar.header("Filters")

default_end = datetime.today()
default_start = default_end - timedelta(days=7)

start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", default_end)

start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

unit = st.sidebar.selectbox(
    "Distanceand Size Unit",
    ["Kilometers", "Miles"]
)

hazard_filter = st.sidebar.selectbox(
    "Hazard Filter",
    ["All", "Hazardous", "Non-Hazardous"]
)

# Valdiation

if start_date > end_date:
    st.error("Start date must be before end date")
    st.stop()

if (end_date - start_date).days > 30:
    st.warning("Please select a range under 30 days")
    st.stop()

# Load data

@st.cache_data(ttl=3600)
def load_data(start_date, end_date, unit, hazard_filter):
    raw_data = get_asteroid_data(start_date, end_date)
    df = process_asteroid_data(raw_data)

    if unit == "Miles":
        df["distance"] = df["miss_distance_miles"]
        df["diameter"] = df["mean_diameter_miles"]
        df["velocity"] = df["velocity_mph"]

        distance_label = "Miss Distance (miles)"
        diameter_label = "Diameter (miles)"
        velocity_label = "Velocity (mph)"

    else:
        df["distance"] = df["miss_distance_km"]
        df["diameter"] = df["mean_diameter_km"]
        df["velocity"] = df["velocity_km_s"]

        distance_label = "Miss Distance (km)"
        diameter_label = "Diameter (km)"
        velocity_label = "Velocity (km/s)"

    filtered_df = df

    if hazard_filter == "Hazardous":
        filtered_df = df[df["is_hazardous"]]

    elif hazard_filter == "Non-Hazardous":
        filtered_df = df[~df["is_hazardous"]]

    return df, filtered_df, distance_label, diameter_label, velocity_label

with st.spinner("Fetching asteroid data..."):
    df, filtered_df, distance_label, diameter_label, velocity_label = load_data(start_date, end_date, unit, hazard_filter)

# Metrics

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Asteroids", len(df))

if hazard_filter == "All":
    col2.metric("Hazardous Asteroids", int(df["is_hazardous"].sum()))
else:
    col2.metric(f"{hazard_filter} Asteroids", len(filtered_df))

col3.metric(
    f"Avg Velocity ({velocity_label.split('(')[-1].replace(')', '')})",
    f"{df['velocity'].mean():.2f}"
)

#Graphs

st.subheader("Asteroid Activity Over Time")
st.caption("Number of asteroids approaching Earth per day.")
st.plotly_chart(
    plot_approaches_over_time(filtered_df), 
    width='stretch'
)

st.subheader("Risk Analysis")
st.write("Shows relationship between distance, velocity, and size to highlight potential threats. ")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        plot_risk_scatter(filtered_df, distance_label, velocity_label),
        width='stretch'
    )

with col2:
    st.plotly_chart(
        plot_top_risk_asteroids(filtered_df),
        width='stretch'
    )

col1, col2 = st.columns(2)

st.subheader("Distribution Insights")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        plot_diameter_distribution(filtered_df, diameter_label),
        width='stretch'
    )

if hazard_filter == "All":
    with col2:
        st.plotly_chart(
            plot_hazardous_counts(filtered_df),
            width='stretch'
        )

st.subheader("Velocity Analysis")

if hazard_filter == "All":
    st.caption("Compare velocity distributions across hazard classifications.")
    st.plotly_chart(
        plot_velocity_box(filtered_df, velocity_label),
        True
    )
else:
    st.caption(f"Velocity distributions for {hazard_filter} asteroids.")
    
    # Single distribution plot instead
    st.plotly_chart(
        plot_velocity_box(filtered_df, velocity_label),
        True
    )