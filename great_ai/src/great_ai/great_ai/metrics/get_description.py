from dash import dcc, html

from ..helper import snake_case_to_text


def get_description(function_name: str, accent_color: str) -> html.Div:
    markdown_text = f"""
    View the live data of your deployments here.

    ## Using the API

    You can find the available endpoints at [/docs](/docs).

    ## Metrics

    Recent traces and aggregated metrics are presented below. Try filtering the table.
    """

    return html.Div(
        [
            html.H1(
                f"{snake_case_to_text(function_name)} - metrics",
                style={"color": accent_color},
            ),
            dcc.Markdown(markdown_text, className="description"),
        ]
    )
