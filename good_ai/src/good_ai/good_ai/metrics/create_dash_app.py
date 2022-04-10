from typing import Any, Dict, List

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
from flask import Flask

from good_ai.utilities.unique import unique

from ..context import get_context
from ..helper import snake_case_to_text
from ..views import SortBy
from .get_description import get_description
from .get_filter_from_datatable import get_filter_from_datatable


def create_dash_app(function_name: str) -> Flask:
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

    app.layout = html.Div(
        [
            get_description(function_name),
            html.Div(
                table := dash_table.DataTable(
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
            ),
            execution_time_histogram := dcc.Graph(),
            parallel_coords := dcc.Graph(),
            interval := dcc.Interval(
                interval=4 * 1000,  # in milliseconds
                n_intervals=0,
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
        df = pd.DataFrame(rows)

        return px.histogram(
            df,
            x="execution_time_ms",
            labels={"execution_time_ms": "Execution time (ms)"},
            nbins=20,
            title="Execution times",
            log_y=True,
        )

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

        df = pd.DataFrame(rows)
        return go.Figure(
            go.Parcoords(
                dimensions=[
                    get_dimension_descriptor(df, c)
                    for c in df.columns
                    if not c.startswith("arg:") and c not in {"id", "created"}
                ]
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
        unique_values = unique(values)
        value_mapping = {str(v): i for i, v in enumerate(unique_values)}

        dimension["values"] = [value_mapping[str(v)] for v in values]
        dimension["tickvals"] = list(value_mapping.values())
        dimension["ticktext"] = list(value_mapping.keys())

    return dimension
