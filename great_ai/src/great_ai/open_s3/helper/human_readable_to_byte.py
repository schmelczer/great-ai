import re


def human_readable_to_byte(size: str) -> int:
    """Case is ignored, kb, kB, Kb, and KB are all treated as kilobyte."""

    if size.strip() == "0":
        return 0

    possible_units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    units_re = "|".join(possible_units)
    regex = re.compile(
        rf"""
        \s*                         # trim
        (?P<scalar>\d+(.\d+)?)      # get scalar, it might be a float
        \s*                         # ignore optional whitespace
        (?P<unit>{units_re})        # capture the unit
    """,
        flags=re.VERBOSE | re.IGNORECASE,
    )

    match = regex.match(size)
    if not match:
        raise ValueError(f'Could not find values in "{size}"')

    results = match.groupdict()

    scalar = float(results["scalar"])
    idx = possible_units.index(results["unit"].upper())
    factor = 1024**idx
    return round(scalar * factor)
