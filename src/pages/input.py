import itertools
import json

import httpx
from fastapi import APIRouter, Request, UploadFile
from fastui import FastUI
from fastui import components as c
from pydantic import BaseModel, ValidationError
from rich import print

from src.pages.shared import base_page
from src.utils.calculator import calculate_ahp, create_ahp_pie_query, flatten_json
from src.utils.constants import (
    enum_selector,
)

router = APIRouter()


class InputSchema(BaseModel):
    criterias: list[str]
    objects: list[str]


@router.get('/input_json', response_model=FastUI, response_model_exclude_none=True)
async def input_json():
    heading = c.Heading(text='Калькулятор метода анализа иерархий', class_name='mb-3')
    file_field = c.FormFieldFile(
        name='file', title='Файл с критериями и объектами сравнения', required=True
    )
    input_json_file_form = c.Form(
        form_fields=[file_field],
        submit_url='/api/calculator/input_json',
    )
    return base_page(heading, input_json_file_form)


@router.post('/input_json', response_model=FastUI, response_model_exclude_none=True)
async def input_json_file(file: UploadFile):
    data = json.load(file.file)
    try:
        input_model = InputSchema.model_validate(data)
    except ValidationError:
        async with httpx.AsyncClient() as client:
            payload = flatten_json(data)
            print(payload)
            response = await client.post(
                'http://127.0.0.1:8000/api/calculator/calculator', json=payload
            )
            response.raise_for_status()
            response_json = response.json()
        return response_json

    criterias_pairs_compares = [
        c.FormFieldSelect(
            name=f'criteria_{s[0]}_{s[1]}',
            title=['Критерий', f'{s[0]} и {s[1]}'],
            options=enum_selector,
            initial='1',
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
            initial='1',
        )
        for s in itertools.product(input_model.criterias, objects_pairs_strings)
    ]

    compare_form = c.Form(
        submit_url='/api/calculator/calculator',
        form_fields=[*criterias_pairs_compares, *objects_pairs_compares],
    )
    return [compare_form]


@router.post('/calculator', response_model=FastUI, response_model_exclude_none=True)
async def calc(request: Request):
    form = await request.form()
    if form:
        data = dict(form)
    else:
        data = await request.json()
        print(data)

    ahp_results = calculate_ahp(data)

    final_image_query = create_ahp_pie_query(ahp_results.final)
    final_image = c.Image(src=f'/api/drawer/draw_chart?{final_image_query}')
    criteria_pie_query = create_ahp_pie_query(ahp_results.criterias)
    criteria_image = c.Image(src=f'/api/drawer/draw_chart?{criteria_pie_query}')

    objects_images = [
        c.Image(src=f'/api/drawer/draw_chart?{create_ahp_pie_query(object)}')
        for object in ahp_results.objects
    ]
    return [
        final_image,
        criteria_image,
        *objects_images,
    ]
