from typing import Optional, Union

from ....views import Filter, operators


def get_filter_from_datatable(description: str) -> Optional[Filter]:
    for operator in operators:
        if operator in description:
            name_part, value_part = description.split(operator, 1)
            value_part = value_part.strip()
            name_part = name_part[name_part.find("{") + 1 : name_part.rfind("}")]

            v0 = value_part[0]
            if v0 == value_part[-1] and v0 in ("'", '"', "`"):
                value: Union[str, float] = value_part[1:-1].replace("\\" + v0, v0)
            else:
                try:
                    value = float(value_part)
                except ValueError:
                    value = value_part
            return Filter(property=name_part, operator=operator, value=value)

    return None
