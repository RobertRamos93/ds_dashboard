import geopandas as gpd
import hvplot.pandas
import pandas as pd

# gdf = gpd.read_file("gpd/inegi_refcenesta_2010.shp", engine="fiona")
# print(gdf.columns)
# print(gdf.head())
# print(gdf["nom_ent"].unique())

def create_mexico_map(df, shapefile_path="gpd/inegi_refcenesta_2010.shp"):
    # Leer shapefile
    gdf = gpd.read_file(shapefile_path, encoding='latin1')
    
    # Mapeo de nombres oficiales
    mapeo_estados = {
        "Veracruz de Ignacio de la Llave": "Veracruz",
        "Distrito Federal": "Ciudad de México"
    }
    gdf["nom_ent"] = gdf["nom_ent"].replace(mapeo_estados)
    
    # Agrupar importes por estado
    importe_por_estado = df.groupby('estado', as_index=False)['importe'].sum()
    
    # Merge con GeoDataFrame
    merged = gdf.merge(importe_por_estado, left_on="nom_ent", right_on="estado", how="left")
    merged['importe'] = merged['importe'].fillna(0)
    
    # Crear múltiples variables para diferentes efectos visuales
    max_importe = merged['importe'].max()
    merged['intensity'] = merged['importe'] / max_importe
    merged['border_width'] = merged['intensity'] * 8 + 1
    merged['alpha_level'] = merged['intensity'] * 0.5 + 0.4
    
    # Mapa principal con bordes dinámicos
    main_map = merged.hvplot.polygons(
        'geometry',
        color='importe',
        geo=True,
        line_color="white",
        line_width='border_width',
        cmap='viridis',
        alpha='alpha_level',
        colorbar=True,
        hover_cols=['nom_ent', 'importe'],
        title="Mapa de México - Efecto de Bordes Dinámicos",
        width=1600,
        height=1000,
        border_multiplier=15
    )
    
    return main_map, merged
