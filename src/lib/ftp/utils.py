import re
from typing import Union


def rename_dict_fields(data: Union[dict, list], regex_expression: str) -> Union[dict, list]:
    """Renames recursively dict keys in provided data"""

    if isinstance(data, list):
        return [rename_dict_fields(data=item, regex_expression=regex_expression) for item in data]
    elif isinstance(data, dict):
        return {
            re.sub(regex_expression, "", key): rename_dict_fields(
                data=value,
                regex_expression=regex_expression
            )
            for key, value in data.items()
        }
    else:
        return data
