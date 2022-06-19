from math import ceil
from typing import Any, Dict, List, Sequence, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from flask import Flask

from great_ai.utilities.unique import unique

from ....constants import DASHBOARD_PATH, ONLINE_TAG_NAME
from ....context import get_context
from ....helper import snake_case_to_text, text_to_hex_color
from ....views import SortBy
from .get_description import get_description
from .get_filter_from_datatable import get_filter_from_datatable
from .get_footer import get_footer
from .get_traces_table import get_traces_table


def create_dash_app(function_name: str, function_docs: str) -> Flask:
    accent_color = text_to_hex_color(function_name)

    app = Dash(
        function_name,
        requests_pathname_prefix=DASHBOARD_PATH + "/",
        server=Flask(__name__),
        title=snake_case_to_text(function_name),
        update_title=None,
        external_stylesheets=[
            "/assets/index.css",
        ],
    )

    app.layout = html.Main(
        [
            html.Div(
                html.P("PRODUCTION" if get_context().is_production else "DEVELOPMENT"),
                className="environment",
            ),
            html.Header(
                [
                    get_description(
                        function_name=function_name,
                        function_docs=function_docs,
                        accent_color=accent_color,
                    ),
                    execution_time_histogram_container := html.Div(),
                ],
            ),
            configuration_container := html.Div(
                className="configuration-container",
            ),
            traces_table_container := html.Div(
                [
                    html.Header(
                        [
                            html.H2("Latest traces"),
                            html.P(
                                "Recent traces and aggregated metrics are presented below. Try filtering the table."
                            ),
                            html.A(
                                "Filtering syntax.",
                                href="https://dash.plotly.com/datatable/filtering",
                                target="_blank",
                            ),
                        ]
                    ),
                    table := get_traces_table(),
                ],
                className="traces-table-container",
            ),
            parallel_coordinates := dcc.Graph(
                className="parallel-coordinates", config={"displaylogo": False}
            ),
            html.Div(className="space-filler"),
            get_footer(),
            interval := dcc.Interval(
                interval=4 * 1000,  # in milliseconds
            ),
        ]
    )

    @app.callback(
        Output(configuration_container, "children"),
        Input(interval, "n_intervals"),
    )
    def update_configuration(
        n_intervals: int,
    ) -> List[html.Div]:
        config = get_context().to_flat_dict()
        return [
            html.Div(
                [
                    html.H4(snake_case_to_text(key)),
                    html.P(str(value)),
                ],
                className="configuration-item",
            )
            for key, value in config.items()
        ]

    @app.callback(
        Output(table, "data"),
        Output(table, "page_count"),
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
        filter_query: str,
        n_intervals: int,
    ) -> Tuple[List[Dict[str, Any]], int]:
        conjunctive_filters = (
            [get_filter_from_datatable(f) for f in filter_query.split(" && ")]
            if filter_query
            else []
        )
        non_null_conjunctive_filters = [f for f in conjunctive_filters if f is not None]

        elements, count = get_context().tracing_database.query(
            skip=page_current * page_size,
            take=page_size,
            conjunctive_tags=[ONLINE_TAG_NAME],
            conjunctive_filters=non_null_conjunctive_filters,
            sort_by=sort_by,
        )

        return (
            [e.to_flat_dict() for e in elements],
            max(1, ceil(count / page_size)),
        )

    @app.callback(
        Output(table, "columns"),
        Output(traces_table_container, "style"),
        Input(interval, "n_intervals"),
    )
    def update_layout(
        n_intervals: int,
    ) -> Tuple[List[Dict[str, Sequence[str]]], Dict[str, Any]]:
        elements, count = get_context().tracing_database.query(
            take=1, conjunctive_tags=[ONLINE_TAG_NAME]
        )

        if elements:
            keys = list(elements[0].to_flat_dict().keys())
            header_height = max(len(i.split(":")) for i in keys)
            columns = [
                {
                    "name": [""] * (header_height - len(k.split(":")))
                    + k.replace("_flat", "").split(":"),
                    "id": k,
                }
                for k in keys
            ]
        else:
            columns = []

        return (
            columns,
            {"display": "block" if count > 0 else "none"},
        )

    @app.callback(
        Output(execution_time_histogram_container, "children"),
        Output(parallel_coordinates, "figure"),
        Output(parallel_coordinates, "style"),
        Input(table, "filter_query"),
        Input(interval, "n_intervals"),
    )
    def update_charts(
        filter_query: str, n_intervals: int
    ) -> Tuple[Any, go.Figure, Dict[str, Any]]:
        conjunctive_filters = (
            [get_filter_from_datatable(f) for f in filter_query.split(" && ")]
            if filter_query
            else []
        )
        non_null_conjunctive_filters = [f for f in conjunctive_filters if f is not None]

        elements, count = get_context().tracing_database.query(
            conjunctive_tags=[ONLINE_TAG_NAME],
            conjunctive_filters=non_null_conjunctive_filters,
        )

        if not elements:
            return (
                html.Span(
                    f"No traces yet: call your function ({function_name}) to create one.",
                    className="placeholder",
                ),
                go.Figure(),
                {"display": "none"},
            )

        flat_elements = [e.to_flat_dict() for e in elements]

        execution_time_histogram = dcc.Graph(config={"displaylogo": False})
        df = pd.DataFrame(flat_elements)
        fig = px.histogram(
            df,
            x="original_execution_time_ms",
            labels={"original_execution_time_ms": "Execution time (ms)"},
            nbins=20,
            height=400,
            log_y=True,
            color_discrete_sequence=[accent_color],
        )
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0, pad=0),
        )
        execution_time_histogram.figure = fig

        parallel_coords_fig = go.Figure(
            go.Parcoords(
                dimensions=[
                    get_dimension_descriptor(df, c)
                    for c in df.columns
                    if c
                    not in {"trace_id", "created", "output", "exception", "feedback"}
                    and "_flat" not in c
                ],
                line_color=accent_color,
            )
        )
        return execution_time_histogram, parallel_coords_fig, {}

    return app.server


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
