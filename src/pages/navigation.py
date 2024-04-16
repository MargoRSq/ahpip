from fastapi import APIRouter
from fastui import FastUI

from src.pages.shared import base_page
from fastui import components as c
from fastui.events import GoToEvent, PageEvent
from src.pages.calculator import calculations_table
