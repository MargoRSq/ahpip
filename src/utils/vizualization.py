def vizalize_ahp_result(ax, colors, target_weights: dict):
    fruits = list(target_weights.keys())
    counts = list(target_weights.values())

    ax.bar(fruits, counts, color=colors)
