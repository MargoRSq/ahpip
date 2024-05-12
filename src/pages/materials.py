from fastapi import APIRouter
from fastui import FastUI
from fastui import components as c

from src.pages.shared import base_page
from src.utils.constants import about_markdown_str

router = APIRouter()


@router.get('/theory', response_model=FastUI, response_model_exclude_none=True)
async def materials():
    about_ahp_markdown = c.Markdown(text=about_markdown_str)
    ahp_tree_image = c.Image(src='/static/ahp_tree.jpeg')
    return base_page(about_ahp_markdown, ahp_tree_image)
