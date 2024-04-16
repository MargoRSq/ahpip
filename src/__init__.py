import os
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastui import prebuilt_html

# from src.pages.input import router as input_router
from src.pages.calculator import router as calculator_router

# from src.pages.navigation import router as navigation_router
# from src.pages.work.first import router as first_router

app = FastAPI()

if getattr(sys, 'frozen', False):
    static_dir = os.path.join(sys._MEIPASS, 'src/static')
else:
    static_dir = 'src/static'
app.mount('/static', StaticFiles(directory=static_dir), name='static')

# app.include_router(input_router, prefix="/api/input")
app.include_router(calculator_router, prefix='/api/calculator')
# app.include_router(navigation_router, prefix="/api/select")


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))
