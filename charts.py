# charts.py
import hvplot.pandas
import pandas as pd
from bokeh.models import NumeralTickFormatter



def popular_products_income(df):
    """Bar chart with the most popular products sold"""

    df_popular_products_income = (
        df.groupby("concepto", as_index=False)["importe"].sum()
    )

    df_popular_products_income["importe"] = df_popular_products_income["importe"] / 1_000_000

    plot_popular_products_income = df_popular_products_income.hvplot(
        kind="bar",
        x="concepto",
        y="importe",
        xlabel="Concepto",
        ylabel="Importe (millones)",
        yformatter=NumeralTickFormatter(format="0,0.0"),
        color="concepto",
        cmap="Category10",
        title="Importe por productos más vendidos",
        rot=90,
        grid=True,
        responsive=True,
        legend="top_left",
        width=1600,
        height=1000
    )

    return df_popular_products_income, plot_popular_products_income

    


