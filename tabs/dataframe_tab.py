import panel as pn
from db_connect import load_data

pn.extension("perspective")

df = load_data()

main_df = pn.pane.Perspective(
    df,
    title="Base de datos VISA",
    editable=True,
    columns_config={"estado": {"string_color_mode": "series", "format": "italics"}},
    sizing_mode="stretch_both"  # quita height fijo
)

main_df_tab = pn.Column(
    main_df,
    pn.layout.VSpacer(),
    sizing_mode="stretch_both"
)