from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastui import prebuilt_html

from src import static_dir
from src.pages.drawer import router as drawer_router
from src.pages.input import router as calculator_router
from src.pages.instruction import router as instruction_router
from src.pages.materials import router as materials_router

app = FastAPI()

app.mount('/static', StaticFiles(directory=static_dir), name='static')

app.include_router(calculator_router, prefix='/api/calculator')
app.include_router(materials_router, prefix='/api/materials')
app.include_router(drawer_router, prefix='/api/drawer')
app.include_router(instruction_router, prefix='/api/instruction')


@app.get('/')
async def redirect_fastapi():
    return RedirectResponse(url='/materials/theory', status_code=302)


paths = ['/', '/materials']
for path in paths:
    app.get(path)(redirect_fastapi)


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='AHP'))
