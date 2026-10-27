import re

pattern = re.compile(
    r"""
        [\t ]*(?P<key>\w+)[\t ]*=[\t ]*
        (?:
              "(?P<double>[^"]*)"
            | '(?P<single>[^']*)'
            | `(?P<backtick>[^`]*)`
            | (?!["'`])(?P<bare>[^\#\r\n]*?)
        )
        [\t ]*(?:\#[^\r\n]*)?(?:\r?\n|$)
    """,
    flags=re.UNICODE | re.VERBOSE,
)

ignored_line = re.compile(r"[\t ]*(?:\#[^\r\n]*)?(?:\r?\n|$)")
