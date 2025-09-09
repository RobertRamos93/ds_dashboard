import panel as pn
import hvplot.pandas
import pandas as pd
from sqlalchemy import create_engine

from geo_map import create_world_map
from plots import trade_value_per_continent_bar_chart, trade_value_per_country_north_america


pn.extension("tabulator")


# def load_data():
#     try:
#         engine = create_engine("postgresql://postgres:Stray@localhost:5432/dashboard_db")
#         df = pd.read_sql_query("SELECT * FROM visa", engine)
#         return df, "Connected to database"
#     except Exception as e:
#         return None, f"Database connection failed: {e}"

# def prepare_data(df):
#     df['importe'] = df['importe'].astype(float)
#     text_cols = ['sucursal', 'concepto', 'tipo']
#     for col in text_cols:
#         df[col] = df[col].astype(str)
#     return df

# df, msg = load_data()
# if df is not None:
#     df = prepare_data(df)
# else:
#     print(msg)

df = pd.read_csv("petroleum.csv")






world_map = create_world_map(df)
continents_bar_chart, continents_df = trade_value_per_continent_bar_chart(df)
country_north_america_chart, country_north_america_df = trade_value_per_country_north_america(df)






# grid = pn.GridBox(
#     bar_chart,
#     per_year,
#     bar_chart,
#     bar_chart,
#     ncols=2,
#     sizing_mode="stretch_width"
# )

continents_bar_chart, continents_df = trade_value_per_continent_bar_chart(df)

continents_df_widget = pn.widgets.Tabulator(
    continents_df,
    theme="bootstrap4",
    page_size=10,
    show_index=False,
    layout="fit_data_stretch",
    selectable=True,
    name="ContinentDataFrameTabulator"
)


north_america_df_widget = pn.widgets.Tabulator(
    country_north_america_df,
    theme="bootstrap4",
    page_size=10,
    show_index=False,
    layout="fit_data_stretch",
    selectable=True,
    name="NorthAmericatDataFrameTabulator"
)

continents_row = pn.Row(
    continents_bar_chart,
    continents_df_widget
)



north_america_row = pn.Row(
    country_north_america_chart,
    continents_df_widget
)

df_widget = pn.widgets.Tabulator(
    df,
    theme="bootstrap4",
    header_align="center",
    text_align="center",
    page_size=25,
    show_index=False,
    # buttons={'csv': 'Download CSV'}, # This button is already built-in for Tabulator
    layout='fit_data_stretch',
    selectable=True,
    configuration={'search': True, 'columnDefaults': {'headerFilter': True}},
    # Make sure to give the Tabulator a name if you want to reference it by string
    name='MyDataFrameTabulator'
)

# Corrected FileDownload using pn.bind or pn.depends
# Option 1: Using pn.bind (often cleaner for simple callbacks)
def get_current_df_for_download_callback():
    # Grab the filtered dataframe from the Tabulator
    current_df = df_widget.current_view
    
    # Encode as CSV bytes
    return current_df.to_csv(index=False).encode("utf-8")

download_csv_widget = pn.widgets.FileDownload(
    callback=get_current_df_for_download_callback,
    filename="database.csv",
    button_type="success",
    label="Download CSV (Filtered)"
)

# Option 2: Using pn.depends (if you prefer this syntax or have more complex dependencies)
# In this case, you depend on the df_widget itself, not its current_view property directly.
@pn.depends(df_widget, watch=True)
def get_current_df_for_download_depends(tabulator_instance):
    # 'tabulator_instance' will be the df_widget object itself
    # When df_widget's internal state changes (like filters being applied),
    # this function will be re-executed, and the FileDownload will update.
    return tabulator_instance.current_view.to_csv(index=False)

download_csv_widget_depends = pn.widgets.FileDownload(
    callback=get_current_df_for_download_depends,
    filename="database_depends.csv",
    button_type="primary",
    label="Download CSV (Filtered, via depends)"
)


dataframe_layout = pn.Column(
    "## Interactive DataFrame",
    df_widget,
    pn.Row(download_csv_widget, download_csv_widget_depends)
)

# PANEL

tabs = pn.Tabs(
    ("World Map", world_map),
    ("Continents", continents_row),
    ("North America", north_america_row),
    ("DataFrame", dataframe_layout)
)



# TextAreaInput
user_input = pn.widgets.TextAreaInput(
    placeholder="Escribe aquí...",
    height=100,
    max_length=1000
)

logo_visa = pn.pane.Image(
    "visa_group.jpg",
    width=200,
    styles={
        'border-radius': '10px',
        'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
        'cursor': 'pointer'
    },
    css_classes=['scale-hover-image']
)



template = pn.template.FastListTemplate(
    title="Visa Group Dashboard",
    sidebar=[
             logo_visa,
             pn.pane.Markdown("# Asistente VisAI"),
             user_input,
             ],
    main=[tabs],
    accent_base_color="#4CAF50",
    header_background="#2E7D32",
)

template.servable()
