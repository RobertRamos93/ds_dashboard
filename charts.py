# charts.py
import hvplot.pandas
import pandas as pd
from bokeh.models import NumeralTickFormatter

def popular_products_income(df, sucursal=None):
    """Bar chart with the most popular products sold, optionally filtered by sucursal"""
    
    # Filter by sucursal if specified
    if sucursal and sucursal != "Todas":
        df_filtered = df[df["sucursal"] == sucursal]
    else:
        df_filtered = df
    
    df_popular_products_income = (
        df_filtered.groupby("concepto", as_index=False)["importe"].sum()
    )

    df_popular_products_income["importe"] = df_popular_products_income["importe"] / 1_000_000

    # Dynamic title based on filter
    title = f"Importe por productos más vendidos"
    if sucursal and sucursal != "Todas":
        title += f" - Sucursal {sucursal}"

    plot_popular_products_income = df_popular_products_income.hvplot(
        kind="bar",
        x="concepto",
        y="importe",
        xlabel="Concepto",
        ylabel="Importe (millones)",
        yformatter=NumeralTickFormatter(format="0,0.0"),
        color="concepto",
        cmap="Category10",
        title=title,
        rot=90,
        grid=True,
        responsive=True,
        legend="top_left",
        width=1600,
        height=1000
    )

    return df_popular_products_income, plot_popular_products_income

def precompute_products_data(df):
    """Pre-compute data and plots for all sucursales"""
    precomputed_data = {}
    
    # Sucursales A, B, C
    sucursales = ["A", "B", "C"]
    
    for sucursal in sucursales:
        df_filtered, plot_filtered = popular_products_income(df, sucursal)
        precomputed_data[sucursal] = {
            "data": df_filtered, 
            "plot": plot_filtered
        }
    
    # Add "Todas" option (all data combined)
    df_all, plot_all = popular_products_income(df, None)
    precomputed_data["Todas"] = {
        "data": df_all,
        "plot": plot_all
    }
    
    return precomputed_data