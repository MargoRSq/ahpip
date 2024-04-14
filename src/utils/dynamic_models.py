import itertools
from pydantic import create_model


def create_pair_names(names: list[str]):
    pairs = list(itertools.combinations(names, 2))
    return [f"{p1} |  {p2}" for p1, p2 in pairs]


def create_dynamic_model(pair_names, criterion, values):
    fields = {"Критерий": (str, criterion)}
    for name, value in zip(pair_names, values):
        fields[name] = (
            float,
            value,
        )  # Значения преобразуем в float для универсальности
    return create_model("DynamicModel", **fields)
