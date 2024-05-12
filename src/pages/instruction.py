from fastapi import APIRouter
from fastui import FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup

from src.pages.shared import base_page
from src.utils.constants import (
    compare_elements,
    instruction_end_markdown_str,
    instruction_start_markdown_str,
)

router = APIRouter()


@router.get('/instruction', response_model=FastUI, response_model_exclude_none=True)
async def materials():
    instruction = [
        c.Markdown(text=instruction_start_markdown_str),
        c.Table(
            data=compare_elements,
            columns=[
                DisplayLookup(
                    field='value',
                    title='Присваиваемая оценка',
                ),
                DisplayLookup(
                    field='desc',
                    title='Результат субъективного сравнения',
                ),
            ],
        ),
        c.Markdown(text=instruction_end_markdown_str),
    ]
    return base_page(*instruction)
