import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from flask import Flask

from good_ai.good_ai.context.get_context import get_context

from ..helper import snake_case_to_text


def create_dash_app(function_name: str) -> Flask:
    app = Dash(function_name, requests_pathname_prefix=get_context().metrics_path + "/")

    markdown_text = f"""
    # {snake_case_to_text(function_name)} - metrics
    > A human-friendly framework for robust end-to-end AI deployments

    ## Using the API

    You can find the available endpoints at [/docs](/docs).

    ## Metrics

    The recent traces and aggregated metrics are presented below.
    """

    df = pd.read_csv(
        "https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv"
    )

    fig = px.scatter(
        df,
        x="gdp per capita",
        y="life expectancy",
        size="population",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=60,
    )

    app.layout = html.Div(
        [
            dcc.Markdown(children=markdown_text),
            dcc.Graph(id="life-exp-vs-gdp", figure=fig),
        ]
    )

    return app.server
