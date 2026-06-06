from dash import dcc, html

from ....helper import snake_case_to_text, strip_lines


def get_description(
    function_name: str, version: str, function_docs: str, accent_color: str
) -> html.Div:
    return html.Div(
        [
            html.H1(
                [
                    f"{snake_case_to_text(function_name)} - dashboard",
                    html.Span(version, className="version-tag"),
                ],
                style={"color": accent_color},
            ),
            dcc.Markdown(
                strip_lines(
                    f"""
                    > View the live data of your deployment here.

                    ## Using the API

                    You can find the available endpoints at [/docs](/docs).

                    ## Details

                    {function_docs}
                """
                ),
                className="description",
            ),
        ]
    )
