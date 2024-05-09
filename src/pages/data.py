import enum
import itertools
import json

from fastui.forms import SelectOption
from pydantic import create_model
from rich import print

from src.utils.dynamic_models import create_pair_names

techs = ['NB-IoT', 'LoRa', 'Стриж', 'URLLC']
techs_pairs = list(itertools.combinations(techs, 2))

print(techs_pairs)

# app.include_router(first_router, prefix="/api/work/first")
comparison_values = {
    'Ёмкость сети': [5, 6, 1 / 3, 1 / 2, 1 / 5, 1 / 5],
    'Энергопотребление передатчика': [1 / 5, 1 / 6, 3, 1 / 2, 5, 6],
    'Пропускная способность канала': [5, 9, 1 / 3, 6, 1 / 6, 1 / 8],
    'Стоимость радиомодуля': [3, 1 / 3, 3, 1 / 6, 4, 5],
    'Радиус действия базовой станции': [2, 3, 4, 1 / 3, 8, 9],
}

criteria_keys = list(comparison_values.keys())
criteria_values = [5, 6, 6, 1, 1 / 5, 5, 2, 3, 1 / 7, 1 / 3]
pair_names_criteria = create_pair_names(criteria_keys)


pair_names_techs = create_pair_names(techs)


with open('data/iot.json') as f:
    data = json.load(f)

# Извлечение массивов
criterias = data['criterias']
criterias_pairs_strings = [
    f'{s[0]} > {s[1]}' for s in list(itertools.combinations(criterias, 2))
]
objects = data['objects']
objects_pairs_strings = [
    f'{s[0]} > {s[1]}' for s in list(itertools.combinations(objects, 2))
]
objects_with_criterias = list(itertools.product(criterias, objects_pairs_strings))
objects_with_string = [f'|{s[0]}| {s[1]}' for s in objects_with_criterias]
print(objects_with_string)


enum_values = {
    'one_nine': '1 / 9',
    'one_eight': '1 / 8',
    'one_seven': '1 / 7',
    'one_six': '1 / 6',
    'one_five': '1 / 5',
    'one_four': '1 / 4',
    'one_three': '1 / 3',
    'one_twop': '1 / 2',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

enum_selector = [
    SelectOption(label=value, value=value) for key, value in enum_values.items()
]

criteria_enums = {}
for criteria in criterias_pairs_strings:
    EnumClass = enum.Enum(criteria, enum_values)
    criteria_enums[criteria] = (EnumClass, enum_values['one'])


objects_enums = {}
for obj in objects_with_string[:2]:
    EnumClass = enum.Enum(obj, enum_values)
    objects_enums[obj] = (EnumClass, enum_values['one'])

InputFormCriterias = create_model('CriteriasModel', **criteria_enums)
InputFormObjects = create_model('ObjectsModel', **objects_enums)
