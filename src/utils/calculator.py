import itertools
from collections import defaultdict
from typing import Any, Optional
from urllib.parse import urlencode

import ahpy
from pydantic import BaseModel, computed_field, field_validator


class AHPModel(BaseModel):
    name: str
    keys: list[str]
    values: list[float]

    @computed_field
    def keys_pairs_tuples(self) -> list[tuple]:
        return list(itertools.combinations(self.keys, 2))

    @computed_field
    def keys_pairs_strings(self) -> list[str]:
        pairs = list(itertools.combinations(self.keys, 2))
        return [f'{p1} |  {p2}' for p1, p2 in pairs]

    @computed_field
    def comparisons(self) -> list[tuple]:
        return dict(zip(self.keys_pairs_tuples, self.values))

    @computed_field
    @property
    def compare_object(self) -> Any:
        return ahpy.Compare(self.name, self.comparisons, precision=4)

    @computed_field
    @property
    def compare_report(self) -> Any:
        return self.compare_object.report(show=False)

    def add_children(self, children):
        self.compare_object.add_children([child.compare_object for child in children])

    @field_validator('values', mode='before')
    def float_numbers(cls, values):
        float_values = []
        for value in values:
            if isinstance(value, str) and '/' in value:
                splited = value.split(' / ')
                value = int(splited[0]) / int(splited[1])
            float_values.append(float(value))
        return float_values


class AHPConclusion(BaseModel):
    name: str
    keys: list[str]
    weights: list[float]
    consistency_ratio: float = 0.0
    model: Optional[AHPModel] = None


class AHPResults(BaseModel):
    criterias: AHPConclusion
    objects: list[AHPConclusion]
    final: AHPConclusion


class SingleComparison(BaseModel):
    key: str
    value: float

    @field_validator('value', mode='before')
    def float_numbers(cls, value):
        if isinstance(value, str) and '/' in value:
            splited = value.split(' / ')
            return int(splited[0]) / int(splited[1])
        return value


def calculate_single_ahp_conclusion(
    name: str, keys: list[str], values: list[str]
) -> AHPConclusion:
    ahp_model = AHPModel(
        name=name,
        keys=keys,
        values=values,
    )
    ahp_report = ahp_model.compare_report
    target_weights = ahp_report['target_weights']
    conslusion = AHPConclusion(
        name=name,
        keys=list(target_weights.keys()),
        weights=list(target_weights.values()),
        consistency_ratio=ahp_model.compare_object.consistency_ratio,
        model=ahp_model,
    )
    return conslusion


def calculate_ahp(data: dict) -> AHPResults:
    criterias_comparisons = [
        SingleComparison(key=key, value=value)
        for key, value in data.items()
        if key.startswith('criteria_')
    ]
    criterias_unique_names = []
    for td in criterias_comparisons:
        if td.key.startswith('criteria_'):
            criteria = td.key.split('_')[1]
            if criteria not in criterias_unique_names:
                criterias_unique_names.append(criteria)
    last_key = next(reversed(data))
    criterias_unique_names.append(last_key.split('_')[1])

    objects = {key: value for key, value in data.items() if key.startswith('object_')}
    objects_unique_names = []
    splited_first_object = list(objects.keys())[0].split('_')
    first_key = splited_first_object[1]
    objects_unique_names.append(splited_first_object[2].split(' и ')[0])
    for key in objects:
        splited_key = key.split('_')
        if splited_key[1] == first_key:
            crits = splited_key[2].split(' и ')
            if crits[1] not in objects_unique_names:
                objects_unique_names.append(crits[1])
        else:
            break
    objects_map = defaultdict(list)
    for key, value in objects.items():
        objects_map[key.split('_')[1]].append(value)

    criteria_conclusion = calculate_single_ahp_conclusion(
        'Критерии', criterias_unique_names, [cr.value for cr in criterias_comparisons]
    )
    objects_conclusions = [
        calculate_single_ahp_conclusion(
            name=key, keys=objects_unique_names, values=values
        )
        for key, values in objects_map.items()
    ]

    final_ahp_object = criteria_conclusion.model.compare_object
    final_ahp_object.add_children(
        [child.model.compare_object for child in objects_conclusions]
    )
    final_target_weights = final_ahp_object['target_weights']
    final_conclusion = AHPConclusion(
        name='Финальное сравнение',
        keys=final_target_weights.keys(),
        weights=final_target_weights.values(),
        consistency_ratio=final_ahp_object.consistency_ratio,
    )
    ahp_results = AHPResults(
        criterias=criteria_conclusion,
        objects=objects_conclusions,
        final=final_conclusion,
    )
    return ahp_results


def create_ahp_pie_query(conclusion: AHPConclusion) -> str:
    query_params = {
        'title': conclusion.name,
        'labels': conclusion.keys,
        'sizes': conclusion.weights,
    }
    query_string = urlencode(query_params, doseq=True)
    return query_string
