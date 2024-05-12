from __future__ import annotations as _annotations

from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent


def base_page(
    *components: AnyComponent, title: str | None = None
) -> list[AnyComponent]:
    return [
        c.PageTitle(text='AHP'),
        c.Navbar(
            title='AHP',
            title_event=GoToEvent(url='/materials/theory'),
            start_links=[
                c.Link(
                    components=[c.Text(text='Теория')],
                    on_click=GoToEvent(url='/materials/theory'),
                    active='startswith:/materials',
                ),
                c.Link(
                    components=[c.Text(text='Инструкция')],
                    on_click=GoToEvent(url='/instruction/instruction'),
                    active='startswith:/instruction',
                ),
                c.Link(
                    components=[c.Text(text='Калькулятор')],
                    on_click=GoToEvent(url='/calculator/input_json'),
                    active='startswith:/calculator',
                ),
            ],
        ),
        c.Page(
            components=[
                *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text='Квартовкин Святослав',
            links=[
                c.Link(
                    components=[c.Text(text='Github')],
                    on_click=GoToEvent(url='https://github.com/margorsq'),
                ),
            ],
        ),
    ]
