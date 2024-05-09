from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastui import prebuilt_html

from src import static_dir
from src.pages.calculator import router as calculator_router
from src.pages.drawer import router as drawer_router
from src.pages.input import router as input_router
from src.pages.materials import router as materials_router

app = FastAPI()

app.mount('/static', StaticFiles(directory=static_dir), name='static')

app.include_router(calculator_router, prefix='/api/calculator')
app.include_router(materials_router, prefix='/api/materials')
app.include_router(input_router, prefix='/api/input')
app.include_router(drawer_router, prefix='/api/drawer')


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))
