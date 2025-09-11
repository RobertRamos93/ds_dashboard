# layout.py
import panel as pn
from db_connect import load_data
from charts import popular_products_income, precompute_products_data
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
    sizing_mode="stretch_width" 
)

# --------------------
# Pre-compute all products data
# --------------------
precomputed_products = precompute_products_data(df)

# --------------------
# Sucursal Filter Widget
# --------------------
sucursal_select = pn.widgets.Select(
    name="Filtrar por Sucursal",
    value="Todas",
    options=["Todas", "A", "B", "C"],
    width=200
)

# --------------------
# Popular products widgets (start with "Todas")
# --------------------
popular_products_income_df_widget = pn.widgets.Tabulator(
    precomputed_products["Todas"]["data"],
    theme="bootstrap4",
    page_size=10,
    show_index=False,
    layout="fit_data",
    selectable=True,
    name="PopularProductsDataFrameTabulator"
)

popular_products_income_plot_pane = pn.pane.HoloViews(
    precomputed_products["Todas"]["plot"]
)

# --------------------
# Callback function to update products view
# --------------------
def update_products_view(event):
    """Update both the plot and table when sucursal selection changes"""
    selected_sucursal = event.new
    
    # Update the table data
    popular_products_income_df_widget.value = precomputed_products[selected_sucursal]["data"]
    
    # Update the plot
    popular_products_income_plot_pane.object = precomputed_products[selected_sucursal]["plot"]

# Watch for changes in the sucursal selector
sucursal_select.param.watch(update_products_view, 'value')

# Create the products layout with filter
popular_products_column = pn.Column(
    pn.Row(sucursal_select, sizing_mode="stretch_width"),
    pn.Row(
        popular_products_income_plot_pane,
        popular_products_income_df_widget,
        sizing_mode="stretch_width"
    ),
    sizing_mode="stretch_width"
)

# --------------------
# Update Data function
# --------------------
def update_data():
    global df, precomputed_products
    df = load_data()
    main_df_widget.value = df

    # Re-compute all products data
    precomputed_products = precompute_products_data(df)
    
    # Update current view with fresh data
    current_sucursal = sucursal_select.value
    popular_products_income_df_widget.value = precomputed_products[current_sucursal]["data"]
    popular_products_income_plot_pane.object = precomputed_products[current_sucursal]["plot"]

    # Recalculate geo map
    mexico_map_plot_pane_new = create_mexico_map(df)
    mexico_map_plot_pane.object = mexico_map_plot_pane_new

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
    ("Products", popular_products_column),
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