import geopandas as gpd
import hvplot.pandas
import pandas as pd
from geopandas import GeoSeries

# gdf = gpd.read_file("gpd/inegi_refcenesta_2010.shp", engine="fiona")
# print(gdf.columns)
# print(gdf.head())

def create_mexico_map(df, shapefile_path="gpd/inegi_refcenesta_2010.shp"):
    # Cargar shapefile de estado
    gdf = gpd.read_file(shapefile_path, engine="fiona")

    # Normalizar nombres de estados para el merge
    gdf['nom_ent'] = gdf['nom_ent'].str.upper()
    df['estado'] = df['estado'].str.upper()

    # Agrupar importes por estado
    importe_por_estado = df.groupby('estado')['importe'].sum().reset_index()

    # Hacer merge con GeoDataFrame
    merged = gdf.merge(importe_por_estado, left_on='nom_ent', right_on='estado', how='left')

    # Limpiar NaNs y reparar geometrías si es necesario
    merged['importe'] = pd.to_numeric(merged['importe'], errors='coerce').fillna(0)
    merged = merged[merged.geometry.is_valid & ~merged.geometry.is_empty]

    # Crear mapa interactivo
    mapa = merged.hvplot.polygons(
        'geometry',
        color='importe',
        geo=True,
        hover_cols=['nom_ent', 'importe'],
        cmap='viridis',
        colorbar=True,
        title="Importe por estado de México",
    )

    return mapa
