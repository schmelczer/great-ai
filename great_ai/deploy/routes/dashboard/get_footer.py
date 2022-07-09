from dash import html

from great_ai import __version__

from ....constants import GITHUB_LINK


def get_footer() -> html.Footer:
    return html.Footer(
        [
            html.Div(
                [
                    html.H6(
                        ["GreatAI", html.Span(__version__, className="version-tag")]
                    ),
                    html.P(
                        "A human-friendly framework for robust end-to-end AI deployments."
                    ),
                ]
            ),
            html.A(
                html.Img(src="/assets/logo.png"),
                href=GITHUB_LINK,
                target="_blank",
            ),
        ],
    )
