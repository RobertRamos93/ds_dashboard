# layout.py
import panel as pn
from db_connect import load_data
from charts import popular_products_income
from geo_map import create_mexico_map

# --------------------
# Panel Extension
# --------------------
pn.extension("tabulator")

# --------------------
# Load DataFrame
# --------------------
df = load_data()

# --------------------
# Main DataFrame widget
# --------------------
main_df_widget = pn.widgets.Tabulator(load_data(),
                                      page_size=10,
                                      sizing_mode="stretch_width")



# --------------------
# Mexico geo map
# --------------------
mexico_map_plot = create_mexico_map(df)

mexico_map_plot_pane = pn.pane.HoloViews(
    mexico_map_plot,
    sizing_mode="stretch_both",
    min_height=400 
)


# --------------------
# Popular products
# --------------------
df_popular_products_income, plot_popular_products_income = popular_products_income(df)

popular_products_income_df_widget = pn.widgets.Tabulator(
    df_popular_products_income,
    theme="bootstrap4",
    page_size=10,
    show_index=False,
    layout="fit_data",
    selectable=True,
    name="PopularProductsDataFrameTabulator"
)

popular_products_income_plot_pane = pn.pane.HoloViews(
    plot_popular_products_income
)

popular_products_row = pn.Row(
    popular_products_income_plot_pane,
    popular_products_income_df_widget,
    sizing_mode="stretch_width"
)


# --------------------
# Update Data function
# --------------------
def update_data():
    df = load_data()
    main_df_widget.value = df

    # Recalculate df/plots
    mexico_map_plot_pane_new = create_mexico_map(df)
    df_popular_products_income_new, plot_popular_products_income_new = popular_products_income(df)

    # update table and plot
    mexico_map_plot_pane.object = mexico_map_plot_pane_new
    popular_products_income_df_widget.value = df_popular_products_income_new
    popular_products_income_plot_pane.object = plot_popular_products_income_new


# --------------------
# Update callback
# --------------------
pn.state.add_periodic_callback(update_data, period=180_000)

# --------------------
# Tabs
# --------------------
tabs = pn.Tabs(
    ("DataFrame", main_df_widget),
    ("Mexico Map", mexico_map_plot_pane),
    ("Products", popular_products_row),
    sizing_mode="stretch_both"
)


# --------------------
# Main template
# --------------------
logo_visa = pn.pane.Image(
    "visa_group.jpg",
    width=200,
)

# TextAreaInput
user_input = pn.widgets.TextAreaInput(
    placeholder="Escribe aquí...",
    height=100,
    max_length=1000
)

dashboard_layout = pn.template.FastListTemplate(
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
