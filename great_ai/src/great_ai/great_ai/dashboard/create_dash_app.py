from typing import Any, Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
from flask import Flask

from great_ai.utilities.unique import unique

from ..context import get_context
from ..helper import snake_case_to_text, text_to_hex_color
from ..views import SortBy
from .get_description import get_description
from .get_filter_from_datatable import get_filter_from_datatable
from .get_footer import get_footer


def create_dash_app(function_name: str, function_docs: str) -> Flask:
    accent_color = text_to_hex_color(function_name)

    flask_app = Flask(__name__)
    app = Dash(
        function_name,
        requests_pathname_prefix=get_context().metrics_path + "/",
        server=flask_app,
        title=snake_case_to_text(function_name),
        update_title=None,
        external_stylesheets=[
            "/assets/index.css",
        ],
    )

    documents = get_context().persistence.get_documents()
    df = pd.DataFrame(documents)

    execution_time_histogram = dcc.Graph(config={"displaylogo": False})
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        page_current=0,
        page_size=20,
        page_action="custom",
        filter_action="custom",
        filter_query="",
        sort_action="custom",
        sort_mode="multi",
        sort_by=[
            {"column_id": "created", "direction": "desc"},
        ],
    )

    app.layout = html.Div(
        [
            html.Div(
                [
                    get_description(
                        function_name=function_name,
                        function_docs=function_docs,
                        accent_color=accent_color,
                    ),
                    execution_time_histogram,
                ],
                className="glance",
            ),
            html.Div([html.H2("Latest traces"), table], className="table-container"),
            parallel_coords := dcc.Graph(
                className="parallel-coords", config={"displaylogo": False}
            ),
            get_footer(),
            interval := dcc.Interval(
                interval=4 * 1000,  # in milliseconds
            ),
        ]
    )

    @app.callback(
        Output(table, "data"),
        Input(table, "page_current"),
        Input(table, "page_size"),
        Input(table, "sort_by"),
        Input(table, "filter_query"),
        Input(interval, "n_intervals"),
    )
    def update_table(
        page_current: int,
        page_size: int,
        sort_by: List[SortBy],
        filter: str,
        n_intervals: int,
    ) -> List[Dict[str, Any]]:
        conjunctive_filters = [
            get_filter_from_datatable(f) for f in filter.split(" && ")
        ]
        non_null_conjunctive_filters = [f for f in conjunctive_filters if f is not None]

        return get_context().persistence.query(
            conjunctive_filters=non_null_conjunctive_filters,
            sort_by=sort_by,
            skip=page_current * page_size,
            take=page_size,
        )

    @app.callback(
        Output(execution_time_histogram, "figure"),
        Input(table, "filter_query"),
        Input(interval, "n_intervals"),
    )
    def update_execution_times(filter: str, _n_intervals: int) -> go.Figure:
        conjunctive_filters = [
            get_filter_from_datatable(f) for f in filter.split(" && ")
        ]
        non_null_conjunctive_filters = [f for f in conjunctive_filters if f is not None]

        rows = get_context().persistence.query(
            conjunctive_filters=non_null_conjunctive_filters
        )

        if not rows:
            return go.Figure()

        df = pd.DataFrame(rows)

        fig = px.histogram(
            df,
            x="execution_time_ms",
            labels={"execution_time_ms": "Execution time (ms)"},
            nbins=20,
            height=400,
            log_y=True,
            color_discrete_sequence=[accent_color],
        )

        fig.update_layout(
            autosize=True,
            margin=dict(l=0, r=0, b=0, t=0, pad=0),
        )

        return fig

    @app.callback(
        Output(parallel_coords, "figure"),
        Input(table, "filter_query"),
        Input(interval, "n_intervals"),
    )
    def update_parallel_coords(filter: str, _n_intervals: int) -> go.Figure:
        conjunctive_filters = [
            get_filter_from_datatable(f) for f in filter.split(" && ")
        ]
        non_null_conjunctive_filters = [f for f in conjunctive_filters if f is not None]

        rows = get_context().persistence.query(
            conjunctive_filters=non_null_conjunctive_filters
        )

        if not rows:
            return go.Figure()

        df = pd.DataFrame(rows)
        return go.Figure(
            go.Parcoords(
                dimensions=[
                    get_dimension_descriptor(df, c)
                    for c in df.columns
                    if c not in {"id", "created", "output"}
                ],
                line_color=accent_color,
            )
        )

    return flask_app


def get_dimension_descriptor(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    dimension: Dict[str, Any] = {
        "label": snake_case_to_text(column),
    }

    values = df[column]

    try:
        dimension["values"] = [float(v) for v in values]
    except (TypeError, ValueError):
        MAX_LENGTH = 40
        unique_values = unique(values)
        value_mapping = {str(v)[-MAX_LENGTH:]: i for i, v in enumerate(unique_values)}

        dimension["values"] = [value_mapping[str(v)[-MAX_LENGTH:]] for v in values]
        dimension["tickvals"] = list(value_mapping.values())
        dimension["ticktext"] = [k[-MAX_LENGTH:] for k in value_mapping.keys()]

    return dimension
