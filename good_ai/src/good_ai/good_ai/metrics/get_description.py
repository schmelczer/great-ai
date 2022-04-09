from dash.dcc import Markdown

from ..helper import snake_case_to_text


def get_description(function_name: str) -> Markdown:
    markdown_text = f"""
    # {snake_case_to_text(function_name)} - metrics
    > A human-friendly framework for robust end-to-end AI deployments

    ## Using the API

    You can find the available endpoints at [/docs](/docs).

    ## Metrics

    The recent traces and aggregated metrics are presented below.
    """

    return Markdown(markdown_text)
