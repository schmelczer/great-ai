from typing import cast

import great_ai.great_ai.context.context as context

from .configure import configure


def get_context() -> context.Context:
    if context._context is None:
        configure()

    return cast(context.Context, context._context)
