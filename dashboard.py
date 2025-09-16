# dashboard.py
import panel as pn
import io
from tabs.dataframe_tab import main_df_tab
from tabs.sucursales_tab import sucursal_a_row
from tabs.geo_map_tab import geo_map_row



# --------------------
# Tabs
# --------------------
tabs = pn.Tabs(
    ("Base de Datos", main_df_tab),
    ("Mexico Map", geo_map_row),
    ("Sucursal A", sucursal_a_row),
)


# --------------------
# Main template
# --------------------

gif_visa = pn.pane.GIF("visa.gif")

# TextAreaInput
user_input = pn.widgets.TextAreaInput(
    placeholder="Escribe aquí...",
    height=100,
    max_length=1000
)

# Create the main dashboard layout first
dashboard_layout = pn.template.FastListTemplate(
    title="Visa Group Dashboard",
    sidebar=[
        gif_visa,
        pn.pane.Markdown("# Asistente VisAI"),
        user_input,
    ],
    main=[tabs],
    accent_base_color="#4CAF50",
    header_background="#2E7D32",
)


# --------------------
# Report button
# --------------------
# Define the callback function now that dashboard_layout exists
def get_report_content():
    """Generates the dashboard report as a file-like object in memory."""
    report_string_io = io.StringIO()
    
    # Save the dashboard layout to the buffer
    dashboard_layout.save(report_string_io, title="Visa Group Report")
    
    # Rewind the buffer to the beginning before returning
    report_string_io.seek(0)
    return report_string_io

# Create the FileDownload widget with the defined callback
download_button = pn.widgets.FileDownload(
    callback=get_report_content,
    filename="visa_group_report.html",
    name="Download Report 📄",
    button_type="primary"
)

# Add the button to the layout's sidebar
dashboard_layout.sidebar.append(download_button)

dashboard_layout = pn.template.FastListTemplate(
    title="Visa Group Dashboard",
    sidebar=[
             gif_visa,
             pn.pane.Markdown("# Asistente VisAI"),
             user_input,
             download_button,
             ],
    main=[tabs],
    accent_base_color="#4CAF50",
    header_background="#2E7D32",
)
dashboard_layout.servable()
