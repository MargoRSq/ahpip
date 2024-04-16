from fastapi import APIRouter
from fastui import FastUI

from src.pages.constants import about_ahp
from src.pages.shared import base_page

router = APIRouter()


@router.get('/theory', response_model=FastUI, response_model_exclude_none=True)
def materials():
    return base_page(*about_ahp)
