from typing import Annotated
from fastapi import APIRouter, UploadFile
from fastui import FastUI
from pydantic import BaseModel
from rich import print

from src.pages.shared import base_page
from fastui import components as c
from fastui.events import GoToEvent, PageEvent
import enum
from collections import defaultdict
from datetime import date
from typing import Annotated, Literal, TypeAlias

from fastapi import APIRouter, Request, UploadFile
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent, PageEvent
from fastui.forms import FormFile, SelectSearchResponse, Textarea, fastui_form
from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator
from pydantic_core import PydanticCustomError

from src.utils.dynamic_models import create_dynamic_model, create_pair_names


router = APIRouter()

techs = ["NB-IoT", "LoRa", "Стриж", "URLLC"]
comparison_values = {
    "Ёмкость сети": [5, 6, 1 / 3, 1 / 2, 1 / 5, 1 / 5],
    "Энергопотребление передатчика": [1 / 5, 1 / 6, 3, 1 / 2, 5, 6],
    "Пропускная способность канала": [5, 9, 1 / 3, 6, 1 / 6, 1 / 8],
    "Стоимость радиомодуля": [3, 1 / 3, 3, 1 / 6, 4, 5],
    "Радиус действия базовой станции": [2, 3, 4, 1 / 3, 8, 9],
}

criteria_keys = list(comparison_values.keys())
criteria_values = [5, 6, 6, 1, 1 / 5, 5, 2, 3, 1 / 7, 1 / 3]
pair_names_criteria = create_pair_names(criteria_keys)


pair_names_techs = create_pair_names(techs)


@router.get("/input", response_model=FastUI, response_model_exclude_none=True)
async def calculator():
    criteria_compare_model = create_dynamic_model(
        pair_names_criteria, criteria_keys, criteria_values
    )

    models = []
    for cr, values in comparison_values.items():
        models.append(create_dynamic_model(pair_names_techs, cr, values))
    return base_page(
        c.Page(
            components=[
                c.Heading(text="Сравнение критериев", level=1),
                c.Table(
                    data=[m() for m in [criteria_compare_model]],
                ),
                c.Heading(text="Сравнение технологий по критериям", level=1),
                c.Table(
                    data=[m() for m in models],
                ),
            ],
        )
    )
