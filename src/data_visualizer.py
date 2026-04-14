import plotly.express as px

def plot_approaches_over_time(df):
    df_counts = df.groupby("date").size().reset_index(name="count")

    fig = px.line(
        df_counts,
        x="date",
        y="count",
        title="Number of Asteroid Approaches Over Time"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Count"
    )

    return fig

def plot_risk_scatter(df, distance_label, velocity_label):
    fig = px.scatter(
        df,
        x="distance",
        y="velocity",
        size="diameter",
        color="is_hazardous",
        hover_name="name",
        log_x=True,
        title="Asteroid Risk Distribution"
    )

    fig.update_layout(
        xaxis_title=distance_label + " (log)",
        yaxis_title=velocity_label
    )

    return fig

def plot_diameter_distribution(df, diameter_label):
    fig = px.histogram(
        df,
        x="diameter",
        nbins=30,
        title="Distribution of Asteroid Sizes"
    )

    fig.update_layout(
        xaxis_title=diameter_label,
        yaxis_title="Count"
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

    fig.update_layout(
        xaxis_title="Is Hazardous",
        yaxis_title="Count"
    )

    return fig

def plot_velocity_box(df, velocity_label):
    fig = px.box(
        df,
        x="is_hazardous",
        y="velocity",
        title="Velocity Distribution by Hazard Level"
    )

    fig.update_layout(
        xaxis_title="Is Hazardous",
        yaxis_title=velocity_label
    )

    return fig

def plot_top_risk_asteroids(df):
    top_df = df.sort_values("risk_score", ascending=False).head(10)

    fig = px.bar(
        top_df,
        x="risk_score",
        y="name",
        hover_name="name",
        orientation="h",
        title="Top 10 Highest Risk Asteroids"
    )

    fig.update_layout(
        xaxis_title="Risk Score",
        yaxis_title="Asteroid"
    )

    return fig