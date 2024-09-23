import dataclasses
import sys
from typing import Union, Type


def get_trade_mark_field_name() -> str:
    """Returns path to trade mark name field"""

    return 'TradeMarkTransactionBody.' \
           'TransactionContentDetails.' \
           'TransactionData.' \
           'TradeMarkDetails.' \
           'TradeMark.' \
           'WordMarkSpecification.' \
           'MarkVerbalElementText'


def create_dataclass_with_non_lists_fields(cls: Type[dataclasses.dataclass],
                                           fields_data: dict) -> dataclasses.dataclass:
    """Creates dataclass with provided data and skips non listed in class fields

    :param cls: class type which need to be
    :param fields_data: dict with key as a class field name and value as a class field value
    :return: created class
    """

    instance = cls()
    for key, value in fields_data.items():
        if key in instance.__dir__():
            instance.__setattr__(key, value)
    return instance


def create_subclasses_in_dict(module_name: str, data: Union[dict, list]) -> Union[dict, list]:
    """
        Recursively creates classes from dict data.
        Gets class name by dict key and creates instance of it with fields data from dict value

    :param module_name: name of module in which classes exist
    :param data: dict or list of dicts with keys as class names and values as these classes data
    :return: dict or list of dicts with created instances inside
    """

    if isinstance(data, dict):
        for key, value in data.items():
            key_class = getattr(sys.modules[module_name], key, None)
            if not key_class:
                continue
            if isinstance(value, list):
                data[key] = [create_dataclass_with_non_lists_fields(
                    cls=key_class,
                    fields_data=create_subclasses_in_dict(module_name=module_name, data=item)
                ) for item in value]
            elif isinstance(value, dict):
                data[key] = create_dataclass_with_non_lists_fields(
                    cls=key_class,
                    fields_data=create_subclasses_in_dict(module_name=module_name, data=value)
                )
            else:
                data[key] = key_class(value)
    return data
