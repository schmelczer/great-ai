from typing import Any, Dict, List, Optional, Union

import pandas as pd
from dash import Dash, dash_table, html
from dash.dependencies import Input, Output
from flask import Flask

from ..context import get_context
from ..views import Filter, SortBy, operators
from .get_description import get_description


def create_dash_app(function_name: str) -> Flask:
    app = Dash(function_name, requests_pathname_prefix=get_context().metrics_path + "/")

    documents = get_context().persistence.get_documents()
    df = pd.DataFrame(documents)

    app.layout = html.Div(
        children=[
            get_description(function_name),
            html.Div(
                dash_table.DataTable(
                    id="table-paging-with-graph",
                    columns=[{"name": i, "id": i} for i in df.columns],
                    page_current=0,
                    page_size=20,
                    page_action="custom",
                    filter_action="custom",
                    filter_query="",
                    sort_action="custom",
                    sort_mode="multi",
                    sort_by=[],
                ),
                style={"height": 750, "overflowY": "scroll"},
            ),
            html.Div(id="table-paging-with-graph-container"),
        ]
    )

    @app.callback(
        Output("table-paging-with-graph", "data"),
        Input("table-paging-with-graph", "page_current"),
        Input("table-paging-with-graph", "page_size"),
        Input("table-paging-with-graph", "sort_by"),
        Input("table-paging-with-graph", "filter_query"),
    )
    def update_table(
        page_current: int, page_size: int, sort_by: List[SortBy], filter: str
    ) -> List[Dict[str, Any]]:
        conjunctive_filters = [get_filter(f) for f in filter.split(" && ")]
        non_null_conjunctive_filters = [f for f in conjunctive_filters if f is not None]

        return get_context().persistence.query(
            conjunctive_filters=non_null_conjunctive_filters,
            sort_by=sort_by,
            skip=page_current * page_size,
            take=page_size,
        )

    # @app.callback(
    #     Output('table-paging-with-graph-container', "children"),
    #     Input('table-paging-with-graph', "data"))
    # def update_graph(rows):
    #     dff = pd.DataFrame(rows)
    #     return html.Div(
    #         [
    #             dcc.Graph(
    #                 id=column,
    #                 figure={
    #                     "data": [
    #                         {
    #                             "x": dff["country"],
    #                             "y": dff[column] if column in dff else [],
    #                             "type": "bar",
    #                             "marker": {"color": "#0074D9"},
    #                         }
    #                     ],
    #                     "layout": {
    #                         "xaxis": {"automargin": True},
    #                         "yaxis": {"automargin": True},
    #                         "height": 250,
    #                         "margin": {"t": 10, "l": 10, "r": 10},
    #                     },
    #                 },
    #             )
    #             for column in ["pop", "lifeExp", "gdpPercap"]
    #         ]
    #     )

    return app.server


def get_filter(description: str) -> Optional[Filter]:
    print(description)
    for operator in operators:
        if operator in description:
            name_part, value_part = description.split(operator, 1)
            value_part = value_part.strip()
            name_part = name_part[name_part.find("{") + 1 : name_part.rfind("}")]

            v0 = value_part[0]
            if v0 == value_part[-1] and v0 in ("'", '"', "`"):
                value: Union[str, float] = value_part[1:-1].replace("\\" + v0, v0)
            else:
                try:
                    value = float(value_part)
                except ValueError:
                    value = value_part
            return Filter(property=name_part, operator=operator, value=value)

    return None
