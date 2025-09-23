import panel as pn
from db_connect import load_data

pn.extension("perspective")

df = load_data()
df_main_clean = df.reset_index(drop=True).drop(columns=["id"])
main_df = pn.pane.Perspective(
    df_main_clean,
    title="Base de datos VISA",
    editable=True,
    columns=[c for c in df_main_clean.columns if c not in ["index", "id"]],  # Add this line!
    columns_config={"estado": {"string_color_mode": "series", "format": "italics"}},
    sizing_mode="stretch_both"
)

main_df_tab = pn.Column(
    main_df,
    pn.layout.VSpacer(),
    sizing_mode="stretch_both"
)