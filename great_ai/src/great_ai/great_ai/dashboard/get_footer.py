from dash import html


def get_footer() -> html.Footer:
    return html.Footer(
        [
            html.Div(
                [
                    html.H6("GreatAI"),
                    html.P(
                        "A human-friendly framework for robust end-to-end AI deployments."
                    ),
                ]
            ),
            html.A(
                html.Img(src="/assets/github.png"),
                href="https://github.com/ScoutinScience/great-ai",
                target="_blank",
            ),
        ],
        className="watermark",
    )
