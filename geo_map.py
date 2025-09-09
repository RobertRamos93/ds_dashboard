import geopandas as gpd
import hvplot.pandas
import pandas as pd

def create_world_map(df):
    """Create world map with trade data"""

    # World geometry
    world = gpd.read_file("gpd/ne_110m_admin_0_countries.shp")

    name_corrections = {
        "United States": "United States of America"
    }

    df_agg = df.groupby(["Country", "Year"], as_index=False)["Trade Value"].sum()

    # Replace names in CSV before merging
    df_agg["Country"] = df_agg["Country"].replace(name_corrections)

    # Merge trade data with world map
    # FIXED: Changed right_on from "COUNTRY" to "Country" to match your DataFrame
    gdf = world.merge(df_agg, left_on="ADMIN", right_on="Country", how="left")
    gdf = gdf.dissolve(by="Country", aggfunc="first").reset_index()



    # Interactive map
    return gdf.hvplot(
        geo=True,
        tiles="CartoLight",
        c="Trade Value",     
        cmap="Viridis",
        hover_cols="Country",  
        line_color="black",
        responsive=True,
        # colorbar=True,  
        logz=True,
        title="World Trade Value Map",
        sizing_mode="stretch_both"
    )
