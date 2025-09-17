# sucursales_tab.py
import hvplot.pandas
import panel as pn
import pandas as pd
from bokeh.models import NumeralTickFormatter
from db_connect import load_data

pn.extension("perspective")

def create_sucursal_a(df):
    """DataFrame widget for Sucursal"""

    df_sucursal_a = df[df["sucursal"] == "A"]
    df_clean = df_sucursal_a.reset_index(drop=True).drop(columns=["id"])


    df_perspective_sucursal_a = pn.pane.Perspective(
    df_clean,
    title="Sucursal A",
    editable=True,
    columns = [c for c in df_sucursal_a.columns if c not in ["index", "id"]],
    columns_config={"estado": {"string_color_mode": "series", "format": "italics"}},
    sizing_mode="stretch_both"  
)
    
    df_sucursal_a_productos = df_sucursal_a.groupby("concepto")["importe"].sum().reset_index()
    sucursal_a_products_plot = df_sucursal_a_productos.hvplot(
        kind="bar",
        x="concepto",
        y="importe",
        xlabel="Concepto",
        rot=90,
        ylabel="Importe",
        color="concepto",
        cmap="Category10",
        title="Venta por concepto - Sucursal A",
        legend="top_left",
        responsive=True
    )
    return df_perspective_sucursal_a, sucursal_a_products_plot

df = load_data()
df_widget_sucursal_a, sucursal_a_products_plot = create_sucursal_a(df)

sucursal_a_row = pn.Row(
    df_widget_sucursal_a,
    sucursal_a_products_plot,
    sizing_mode="stretch_both"
)