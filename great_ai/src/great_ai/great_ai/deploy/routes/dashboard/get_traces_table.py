from dash import dash_table


def get_traces_table() -> dash_table.DataTable:
    return dash_table.DataTable(
        page_current=0,
        page_size=20,
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
            "overflow": "hidden",
            "text-overflow": "ellipsis",
        },
        style_cell={"padding": "5px"},
        style_header={
            "background-color": "white",
            "font-weight": "bold",
        },
        style_table={"max-height": "70vh", "overflow": "auto"},
        merge_duplicate_headers=True,
        style_cell_conditional=[
            {"if": {"column_id": "output"}, "width": 1500},
        ],
    )
