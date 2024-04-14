from fastapi import APIRouter
from fastui import FastUI

from src.pages.shared import base_page
from fastui import components as c
from fastui.events import GoToEvent, PageEvent


router = APIRouter()


@router.get("/main", response_model=FastUI, response_model_exclude_none=True)
def calculator():
    return base_page()
