# dashboard.py
import panel as pn
import io
from tabs.dataframe_tab import main_df_tab
from tabs.sucursales_tab import sucursal_a_row
from tabs.geo_map_tab import geo_map_row
from llm import chat_ui


# --------------------
# Tabs
# --------------------
tabs = pn.Tabs(
    ("Base de Datos", main_df_tab),
    ("Mexico Map", geo_map_row),
    ("Sucursal A", sucursal_a_row),
)


# --------------------
# Report Download Function
# --------------------
def get_report_content():
    """Generates the dashboard report as a file-like object in memory."""
    report_string_io = io.StringIO()
    
    # Save the dashboard layout to the buffer
    dashboard_layout.save(report_string_io, title="Visa Group Report")
    
    # Rewind the buffer to the beginning before returning
    report_string_io.seek(0)
    return report_string_io


# --------------------
# Download Button
# --------------------
download_button = pn.widgets.FileDownload(
    callback=get_report_content,
    filename="visa_group_report.html",
    label="Descargar Reporte",
    button_type="success",
    icon="download",
    icon_size="20px",
    width=150
)


# --------------------
# Sidebar Components
# --------------------
gif_visa = pn.pane.GIF("visa.gif")

# Line separator
separator = pn.pane.HTML("<hr style='border: 1px solid #ddd; margin: 20px 0;'>")


# --------------------
# Main Dashboard Layout
# --------------------
dashboard_layout = pn.template.FastListTemplate(
    title="Visa Group Dashboard",
    logo="visa_group.jpg",
    sidebar=[
        gif_visa,
        separator,  # Line separator between GIF and chat
        chat_ui,
    ],
    main=[tabs],
    header=[download_button],  # Download button in header
    theme_toggle=True,
    accent="#032876"
)

dashboard_layout.servable()