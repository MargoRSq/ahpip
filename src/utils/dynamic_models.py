import itertools

from pydantic import create_model


def create_pair_names(names: list[str]):
    pairs = list(itertools.combinations(names, 2))
    return [f'{p1} |  {p2}' for p1, p2 in pairs]


def create_dynamic_model(pair_names, name_field_key, name_field_value, values):
    fields = {name_field_key: (str, name_field_value)}
    for name, value in zip(list(pair_names), list(values)):
        fields[name] = (
            float,
            value,
        )  # Значения преобразуем в float для универсальности
    return create_model('DynamicModel', **fields)
