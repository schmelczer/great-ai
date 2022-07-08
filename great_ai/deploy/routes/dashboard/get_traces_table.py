from dash import dash_table

from ....context import get_context


def get_traces_table() -> dash_table.DataTable:
    return dash_table.DataTable(
        page_current=0,
        page_size=get_context().dashboard_table_size,
        page_action="custom",
        filter_action="custom",
        sort_action="custom",
        sort_mode="multi",
        sort_by=[
            {"column_id": "created", "direction": "desc"},
        ],
        style_data={
            "white-space": "normal",
            "height": "auto",
            "max-height": "300px",
            "max-width": "500px",
            "overflow": "hidden",
        },
        style_cell={"padding": "5px"},
        style_header={
            "background-color": "white",
            "font-weight": "bold",
        },
        merge_duplicate_headers=True,
        style_table={"overflow": "auto", "max-height": "80vh"},
    )
