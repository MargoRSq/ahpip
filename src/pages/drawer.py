from io import BytesIO
from typing import List

import numpy as np
from fastapi import APIRouter, Query, Response
from matplotlib import pyplot as plt


def draw_pie(labels: list[str], sizes: list[float]) -> BytesIO:
    colors = plt.cm.Blues(np.linspace(0.2, 1, len(labels)))

    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(
        sizes, colors=colors, autopct='%1.1f%%', pctdistance=0.75
    )
    plt.setp(
        autotexts,
        size=8,
        color='white',
        weight='bold',
        bbox=dict(boxstyle='square,pad=0.3', facecolor='black', edgecolor='none'),
    )
    ax.legend(
        wedges,
        labels,
        loc='center left',
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.subplots_adjust(right=0.75)  # Оставляем место для легенды

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    return buf


router = APIRouter()


@router.get('/draw_chart')
def draw(labels: List[str] = Query(...), sizes: List[float] = Query(...)):
    img_bytes = draw_pie(labels=labels, sizes=sizes)
    return Response(content=img_bytes.read(), media_type='image/png')
