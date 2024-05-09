import itertools
import json
from typing import Annotated
from urllib.parse import urlencode

import matplotlib
from fastapi import APIRouter, Request, UploadFile
from fastui import FastUI
from fastui import components as c
from fastui.forms import SelectOption, fastui_form
from matplotlib import pyplot as plt
from pydantic import BaseModel, field_validator
from rich import print

from src.pages.calculator import AHPModel
from src.pages.data import (
    InputFormCriterias,
    InputFormObjects,
    criterias,
    enum_selector,
    enum_values,
)
from src.pages.shared import base_page

matplotlib.use('Agg')
router = APIRouter()

plt.ioff()


class InputSchema(BaseModel):
    criterias: list[str]
    objects: list[str]


@router.get('/input_json', response_model=FastUI, response_model_exclude_none=True)
async def input_json():
    file_field = c.FormFieldFile(name='file', title='Файлик', required=True)
    return base_page(
        c.Form(form_fields=[file_field], submit_url='/api/input/input_json')
    )


@router.post('/input_json', response_model=FastUI, response_model_exclude_none=True)
async def input_json_file(file: UploadFile):
    data = json.load(file.file)
    input_model = InputSchema.model_validate(data)
    criterias_pairs_compares = [
        c.FormFieldSelect(
            name=f'criteria_{s[0]}_{s[1]}',
            title=['Критерий', f'{s[0]} и {s[1]}'],
            options=enum_selector,
            initial=enum_values['one'],
            required=True,
        )
        for s in itertools.combinations(input_model.criterias, 2)
    ]
    objects_pairs_strings = [
        f'{s[0]} и {s[1]}' for s in itertools.combinations(input_model.objects, 2)
    ]
    objects_pairs_compares = [
        c.FormFieldSelect(
            name=f'object_{s[0]}_{s[1]}',
            title=['Сравнение по критерию', s[0], f'{s[1]}'],
            options=enum_selector,
            required=True,
            initial=enum_values['one'],
        )
        for s in itertools.product(input_model.criterias, objects_pairs_strings)
    ]
    # print(list(itertools.combinations(input_model.criterias, 2)))
    return [
        c.Heading(text='Попарные сравнения', level=2),
        c.Form(
            submit_url='/api/input/calculator',
            form_fields=[*criterias_pairs_compares, *objects_pairs_compares],
        ),
    ]


class Tdata(BaseModel):
    comp: str
    val: float

    @field_validator('val', mode='before')
    def float_numbers(cls, value):
        if isinstance(value, str) and '/' in value:
            splited = value.split(' / ')
            return int(splited[0]) / int(splited[1])
        return value


# def map_compares_to


@router.post('/calculator', response_model=FastUI, response_model_exclude_none=True)
async def calc(request: Request):
    form = await request.form()
    data = dict(form)
    print(data)

    criterias_values = [
        value for key, value in data.items() if key.startswith('criteria_')
    ]
    criterias = []
    for key, _ in data.items():
        if key.startswith('criteria_'):
            criteria = key.split('_')[1]
            if criteria not in criterias:
                criterias.append(criteria)
    last_key = next(reversed(data))
    criterias.append(last_key.split('_')[1])
    print(criterias)

    criteria_model = AHPModel(
        name='Критерии',
        keys=criterias,
        values=criterias_values,
    )
    final_ahp = criteria_model.compare_report
    target_weights = final_ahp['target_weights']
    target_data = []
    for k, v in final_ahp['target_weights'].items():
        target_data.append(Tdata(comp=k, val=v))

    query_params = {
        'labels': list(target_weights.keys()),
        'sizes': list(target_weights.values()),
    }
    query_string = urlencode(query_params, doseq=True)

    return base_page(
        c.Image(src=f'/api/drawer/draw_chart?{query_string}'),
        c.Div(
            components=[
                c.Table(data=target_data),
            ],
            class_name='d-flex justify-content-center',
        ),
    )


# -----------------------------------------------------------------------------


@router.get('/input', response_model=FastUI, response_model_exclude_none=True)
def materials():
    return base_page(
        c.ModelForm(
            model=InputFormCriterias,
            display_mode='default',
            submit_url='/api/input/inputer',
            method='POST',
        )
    )


class Tdata(BaseModel):
    comp: str
    val: float

    @field_validator('val', mode='before')
    def float_numbers(cls, value):
        if isinstance(value, str) and '/' in value:
            splited = value.split(' / ')
            return int(splited[0]) / int(splited[1])
        return value


@router.post('/inputer', response_model=FastUI, response_model_exclude_none=True)
def inputer(form: Annotated[InputFormCriterias, fastui_form(InputFormCriterias)]):
    # print(type(form))
    data = []
    for k, v in form.model_dump().items():
        data.append(Tdata(comp=k, val=v.value))

    criteria_model = AHPModel(
        name='Критерии',
        keys=criterias,
        values=[d.val for d in data],
    )
    final_ahp = criteria_model.compare_report

    target_weights = final_ahp['target_weights']
    target_data = []
    for k, v in final_ahp['target_weights'].items():
        target_data.append(Tdata(comp=k, val=v))

    f = c.ModelForm(
        model=InputFormObjects,
        display_mode='default',
        submit_url='/api/input/outputer',
        method='POST',
    )
    print(f)
    query_params = {
        'labels': list(target_weights.keys()),
        'sizes': list(target_weights.values()),
    }
    query_string = urlencode(query_params, doseq=True)

    return base_page(
        c.Image(src=f'/api/drawer/draw_chart?{query_string}'),
        c.Div(
            components=[
                c.Table(data=target_data),
            ],
            class_name='d-flex justify-content-center',
        ),
        f,
    )


@router.post('/outputer', response_model=FastUI, response_model_exclude_none=True)
def kek(form: Annotated[InputFormObjects, fastui_form(InputFormObjects)]):
    print(form)
    return []


@router.get('/test', response_model=FastUI, response_model_exclude_none=True)
def lol():
    address_options = [
        SelectOption(value='12', label=f'lOl{address}') for address in [1, 2]
    ]
    booking_select_field = c.forms.FormFieldSelect(
        options=address_options,
        title='sElect booking address',
        name='select_address',
        multiple=False,
        placeholder='123',
    )

    booking_form = c.Form(
        form_fields=[booking_select_field],
        submit_url='/api/input/testing',
    )
    # print(booking_form)
    return base_page(booking_form)


@router.post('/testing')
async def post_lol(request: Request):
    f = await request.form()
    print(dict(f))
    return base_page(c.Text(text='1'))
