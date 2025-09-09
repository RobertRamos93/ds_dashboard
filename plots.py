# plots.py
import hvplot.pandas
import pandas as pd


def trade_value_per_continent_bar_chart(df):
    """Bar chart containing trade value per continent"""

    df_trade_value_per_continent = (
        df.groupby("Continent", as_index=False)["Trade Value"].sum()
    )

    return df_trade_value_per_continent.hvplot(
        kind="bar",
        x="Continent",
        y="Trade Value",
        color="Continent",
        cmap="Category10",
        title="Trade value per continent",
        rot=90,
        fontscale=1.5,
        grid=True,
        responsive=True,
        legend="top_left",
        width=1400,
        height=800
    ), df_trade_value_per_continent


def trade_value_per_country_north_america(df):
    """Hi"""

    country_north_america = (
    df[df["Continent"] == "North America"]
    .groupby("Country")
    .agg({"Trade Value": ["sum", "mean", "max"]})
)

    # Flatten column names
    country_north_america.columns = ['_'.join(col).strip() if type(col) is tuple else col for col in country_north_america.columns]

    df_country_north_america = country_north_america.reset_index()


    return country_north_america.hvplot(
    kind="bar",
    x="Country",
    y="Trade Value_sum",
    color="Country",
    cmap="Set2",
    title="Trade value per country in North America",
    rot=90,
    fontscale=1.15,
    grid=True,
    height=1000,
    width=1800,
    legend="bottom",
    legend_cols=4
), df_country_north_america

