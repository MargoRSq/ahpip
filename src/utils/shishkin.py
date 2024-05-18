# import itertools

# import ahpy
# from rich import print, traceback

# traceback.install(show_locals=False)

# comparison_values = {
#     'Ёмкость сети': [5, 6, 1 / 3, 1 / 2, 1 / 5, 1 / 5],
#     'Энергопотребление передатчика': [1 / 5, 1 / 6, 3, 1 / 2, 5, 6],
#     'Пропускная способность канала': [5, 9, 1 / 3, 6, 1 / 6, 1 / 8],
#     'Стоимость радиомодуля': [3, 1 / 3, 3, 1 / 6, 4, 5],
#     'Радиус действия базовой станции': [2, 3, 4, 1 / 3, 8, 9],
# }
# comparison_values = {
#     'Ёмкость сети': [1, 1, 1, 1, 1, 1, 1],
#     'Энергопотребление передатчика': [1, 1, 1, 1, 1, 1, 1],
#     'Пропускная способность канала': [1, 1, 1, 1, 1, 1, 1],
#     'Стоимость радиомодуля': [1, 1, 1, 1, 1, 1, 1],
#     'Радиус действия базовой станции': [1, 1, 1, 1, 1, 1, 1],
# }

# PRECISION = 3

# criteria = [
#     'Ёмкость сети',
#     'Энергопотребление передатчика',
#     'Пропускная способность канала',
#     'Стоимость радиомодуля',
#     'Радиус действия базовой станции',
# ]
# criteria_pairs = list(itertools.combinations(criteria, 2))
criteria_values = [5, 6, 6, 1,
                    1 / 5, 5, 2,
                      3, 1 / 7,
                        1 / 3]
# criteria_comparisons = dict(zip(criteria_pairs, criteria_values))

# techs = ['NB-IoT', 'LoRa', 'Стриж', 'URLLC']
# techs_pairs = list(itertools.combinations(techs, 2))

# capacity_values = [5, 6, 1 / 3, 1 / 2, 1 / 5, 1 / 5]
# capacity_comparisons = dict(zip(techs_pairs, capacity_values))
# energy_values = [1 / 5, 1 / 6, 3, 1 / 2, 5, 6]
# energy_comparisons = dict(zip(techs_pairs, energy_values))
# throughput_values = [5, 9, 1 / 3, 6, 1 / 6, 1 / 8]
# throughput_comparisons = dict(zip(techs_pairs, throughput_values))
# cost_values = [3, 1 / 3, 3, 1 / 6, 4, 5]
# cost_comparisons = dict(zip(techs_pairs, cost_values))
# radius_values = [2, 3, 4, 1 / 3, 8, 9]
# radius_comparisons = dict(zip(techs_pairs, radius_values))


# criteria = ahpy.Compare('Criteria', criteria_comparisons, precision=PRECISION)


# capacity = ahpy.Compare('Ёмкость сети', capacity_comparisons, precision=PRECISION)
# energy = ahpy.Compare(
#     'Энергопотребление передатчика', energy_comparisons, precision=PRECISION
# )
# throughput = ahpy.Compare(
#     'Пропускная способность канала', throughput_comparisons, precision=PRECISION
# )
# cost = ahpy.Compare('Стоимость радиомодуля', cost_comparisons, precision=PRECISION)
# radius = ahpy.Compare(
#     'Радиус действия базовой станции', radius_comparisons, precision=PRECISION
# )

# criteria.add_children([capacity, energy, throughput, cost, radius])
# # criteria.add_children([capacity])

# # print(criteria.target_weights, criteria.consistency_ratio)
# # print(sum(criteria.target_weights.values()))
# # print(radius.report(show=False)["elements"])
# report = criteria.report(show=False)
# # print(report)


# def main():
#     # vizalize_ahp_result(report["target_weights"])
#     print(radius.report())
#     print(report)
#     # fig, (ax0, ax1) = plt.subplots(2)
#     # colors = [[np.random.random_sample() for _ in range(3)] for _ in range(4)]
#     # vizalize_ahp_result(ax0, colors, energy.report()["elements"]["local_weights"])
#     # vizalize_ahp_result(ax1, colors, report["target_weights"])
#     # plt.show()


# main()
# # print(criteria.report(show=False))
