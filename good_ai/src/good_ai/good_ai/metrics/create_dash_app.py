import pandas as pd
from dash import Dash, dash_table, html
from dash.dependencies import Input, Output
from flask import Flask

from good_ai.good_ai.context.get_context import get_context

from .get_description import get_description


def create_dash_app(function_name: str) -> Flask:
    app = Dash(function_name, requests_pathname_prefix=get_context().metrics_path + "/")

    documents = get_context().persistence.get_documents()

    df = pd.DataFrame(
        [
            {
                "id": d.evaluation_id,
                "created": d.created,
                "execution_time_ms": d.execution_time_ms,
                "models": ", ".join(f"{m.key}:{m.version}" for m in d.models),
                "evaluation": d.evaluation,
                **d.logged_values,
            }
            for d in documents
        ]
    )
    print(df)

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
                className="six columns",
            ),
            html.Div(id="table-paging-with-graph-container", className="five columns"),
        ]
    )

    operators = [
        ["ge ", ">="],
        ["le ", "<="],
        ["lt ", "<"],
        ["gt ", ">"],
        ["ne ", "!="],
        ["eq ", "="],
        ["contains "],
        ["datestartswith "],
    ]

    def split_filter_part(filter_part):
        for operator_type in operators:
            for operator in operator_type:
                if operator in filter_part:
                    name_part, value_part = filter_part.split(operator, 1)
                    name = name_part[name_part.find("{") + 1 : name_part.rfind("}")]

                    value_part = value_part.strip()
                    v0 = value_part[0]
                    if v0 == value_part[-1] and v0 in ("'", '"', "`"):
                        value = value_part[1:-1].replace("\\" + v0, v0)
                    else:
                        try:
                            value = float(value_part)
                        except ValueError:
                            value = value_part

                    # word operators need spaces after them in the filter string,
                    # but we don't want these later
                    return name, operator_type[0].strip(), value

        return [None] * 3

    @app.callback(
        Output("table-paging-with-graph", "data"),
        Input("table-paging-with-graph", "page_current"),
        Input("table-paging-with-graph", "page_size"),
        Input("table-paging-with-graph", "sort_by"),
        Input("table-paging-with-graph", "filter_query"),
    )
    def update_table(page_current, page_size, sort_by, filter):
        filtering_expressions = filter.split(" && ")
        dff = df
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ("eq", "ne", "lt", "le", "gt", "ge"):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == "contains":
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == "datestartswith":
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]

        if len(sort_by):
            dff = dff.sort_values(
                [col["column_id"] for col in sort_by],
                ascending=[col["direction"] == "asc" for col in sort_by],
                inplace=False,
            )

        return dff.iloc[
            page_current * page_size : (page_current + 1) * page_size
        ].to_dict("records")

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
