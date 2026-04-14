import plotly.express as px

def plot_approaches_over_time(df):
    df_counts = df.groupby("date").size().reset_index(name="count")

    fig = px.line(
        df_counts,
        x="date",
        y="count",
        title="Number of Asteroid Approaches Over Time"
    )

    return fig

def plot_risk_scatter(df):
    fig = px.scatter(
        df,
        x="miss_distance_km",
        y="velocity_km_s",
        size="mean_diameter",
        color="is_hazardous",
        hover_name="name",
        title="Asteroid Risk Distribution"
    )

    return fig

def plot_diameter_distribution(df):
    fig = px.histogram(
        df,
        x="mean_diameter",
        nbins=30,
        title="Distribution of Asteroid Sizes"
    )

    return fig

def plot_hazardous_counts(df):
    counts = df["is_hazardous"].value_counts().reset_index()
    counts.columns = ["is_hazardous", "count"]

    fig = px.bar(
        counts,
        x="is_hazardous",
        y="count",
        title="Hazardous vs Non-Hazardous Asteroids"
    )

    return fig

def plot_velocity_box(df):
    fig = px.box(
        df,
        x="is_hazardous",
        y="velocity_km_s",
        title="Velocity Distribution by Hazard Level"
    )

    return fig