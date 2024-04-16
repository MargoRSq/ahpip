import itertools

from src.utils.dynamic_models import create_pair_names

techs = ['NB-IoT', 'LoRa', 'Стриж', 'URLLC']
techs_pairs = list(itertools.combinations(techs, 2))
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
