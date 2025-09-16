import geopandas as gpd
import hvplot.pandas
import pandas as pd
import holoviews as hv
import panel as pn
from db_connect import load_data

hv.extension('bokeh')

def create_mexico_map(df, shapefile_path="gpd/inegi_refcenesta_2010.shp"):
    # Leer shapefile
    gdf = gpd.read_file(shapefile_path, encoding='latin1')
    
    # Mapeo de nombres oficiales
    mapeo_estados = {
        "Veracruz de Ignacio de la Llave": "Veracruz",
        "Distrito Federal": "CDMX",
        "Michoacán de Ocampo": "Michoacan"
    }
    gdf["nom_ent"] = gdf["nom_ent"].replace(mapeo_estados)
    
    # Agrupar importes por estado
    df_importe_por_estado = df.groupby('estado', as_index=False)['importe'].sum()

    geo_map_df = pn.pane.Perspective(
    df_importe_por_estado,
    title="Importe por estado",
    editable=True,
    columns=["estado", "importe"],
    columns_config={"estado": {"string_color_mode": "series", "format": "italics"}},
    sizing_mode="stretch_both"  # quita height fijo
)
    
    # Merge
    merged = gdf.merge(df_importe_por_estado, left_on="nom_ent", right_on="estado", how="left")
    merged['importe'] = merged['importe'].fillna(0)
    
    # Importes en millones
    merged['importe_millones'] = merged['importe'] / 1_000_000
    merged['importe_fmt'] = merged['importe_millones'].apply(lambda x: f"${x:,.2f}M")
    
    # Porcentaje
    total = merged['importe'].sum()
    merged['porcentaje'] = (merged['importe'] / total * 100).round(2).astype(str) + '%'
    
    # Separar estados con valores > 0
    colored = merged[merged['importe_millones'] > 0]
    
    # Capa de bordes: todos los estados, sin relleno
    borders = merged.hvplot.polygons(
        'geometry',
        geo=True,
        line_color="black",
        line_width=1,
        fill_alpha=0,      # sin relleno
        hover_cols=[]
    )
    
    # Capa de colores: solo estados con valores
    colored_layer = colored.hvplot.polygons(
        'geometry',
        color='importe_millones',
        geo=True,
        line_color="black",
        line_width=1,
        cmap='viridis',
        alpha=1.0,
        colorbar=True,
        hover_cols=['nom_ent', 'importe_fmt', 'porcentaje']
    ).opts(
        clim=(0, colored['importe_millones'].max()),
        colorbar_opts={'title': 'Millones'}
    )
    
    # Combinar capas
    mapa_mexico = borders * colored_layer
    
    
    return geo_map_df, mapa_mexico

df = load_data()
geo_map_df, mapa_mexico_plot = create_mexico_map(df)



geo_map_row = pn.Row(
    (geo_map_df, {"flex": 1}),
    (mapa_mexico_plot, {"flex": 2}),
    sizing_mode="stretch_both"
)