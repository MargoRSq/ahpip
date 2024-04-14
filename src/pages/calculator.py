import itertools
import os
from typing import Annotated, Any
from fastapi import APIRouter, UploadFile
from fastui import FastUI
from matplotlib import pyplot as plt
from pydantic import BaseModel, computed_field
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
import ahpy

from src.pages.data import comparison_values, pair_names_techs, techs_pairs, techs

router = APIRouter()


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
        return [f"{p1} |  {p2}" for p1, p2 in pairs]

    @computed_field
    def comparisons(self) -> list[tuple]:
        return dict(zip(self.keys_pairs_tuples, self.values))

    @computed_field
    @property
    def compare_object(self) -> Any:
        return ahpy.Compare(self.name, self.comparisons, precision=3)

    @computed_field
    @property
    def compare_report(self) -> Any:
        return self.compare_object.report(show=False)

    def add_children(self, children):
        self.compare_object.add_children([child.compare_object for child in children])


criteria_model = AHPModel(
    name="Критерии",
    keys=list(comparison_values.keys()),
    values=[5, 6, 6, 1, 1 / 5, 5, 2, 3, 1 / 7, 1 / 3],
)

all_compares = [
    AHPModel(name=key, keys=techs, values=value)
    for key, value in comparison_values.items()
]

final_ahp = criteria_model.compare_object
final_ahp.add_children([child.compare_object for child in all_compares])
final_report = final_ahp.report()


row_model = create_dynamic_model(
    pair_names=final_ahp["target_weights"].keys(),
    name_field_key="Критерии",
    name_field_value="Итог",
    values=final_ahp["target_weights"].values(),
)

comps = []


def generate_model(row_model, target_weights, name):
    m = row_model(
        Критерии=name,
        **target_weights,
    )
    fig, ax = plt.subplots()
    ax.bar(
        list(target_weights.keys()),
        list(target_weights.values()),
        label="Sample Data",
        align="center",
    )
    ax.set_ylim(ymax=1)
    if not os.path.exists("static"):
        os.makedirs("static")
    path = f"src/static/{name}.png"
    plt.savefig(path)
    plt.close()
    return m


for i, row in enumerate(all_compares):
    m = generate_model(row_model, row.compare_report["target_weights"], row.name)
    comps.append(m)

result_m = generate_model(row_model, final_report["target_weights"], "Итог")

print(final_report["target_weights"])


@router.get("/calulations", response_model=FastUI, response_model_exclude_none=True)
def calculations_table():
    return base_page(
        c.Page(
            components=[
                c.Div(
                    components=[
                        c.Heading(
                            text="Сравнение технологий по критериям",
                            level=1,
                        ),
                        c.Image(src=f"/static/{result_m.Критерии}.png", width="50%"),
                        c.Table(
                            data=[result_m],
                        ),
                    ],
                    class_name="pb-3",
                ),
                *[
                    c.Div(
                        components=[
                            c.Heading(text=model.Критерии, level=3),
                            c.Image(src=f"/static/{model.Критерии}.png", width="50%"),
                            c.Table(data=[model]),
                        ],
                        class_name="border-top mt-3 pt-3",
                    )
                    for model in comps
                ],
            ],
        )
    )
