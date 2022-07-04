import re

pattern = re.compile(
    r"""
        (?:^|\n)        # new key-value pairs must start on a new line
        \s*             # leading whitespace is allowed
        (?!\#)          # the key cannot start with a `#` symbol
        (\w+?)          # then comes the key
        \s*=\s*         # the key and value are separated by an equal sign
        (?:             # then comes the value
              "([^"]*)"   # the value can be surrounded by quotes: "value"
            | '([^']*)'   # the value can be surrounded by quotes: 'value'
            | `([^`]*)`   # the value can be surrounded by quotes: `value`
            | ([^#\n]*?)  # or it is bare, in that case, the trailing whitespace is ignored
        )
        \s*(?:\#.*)?    # comments can be added with the `#` symbol
        (?=\n|$)        # a key-value pairs are separated by new lines
    """,
    flags=re.UNICODE | re.VERBOSE,
)
