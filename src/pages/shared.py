from __future__ import annotations as _annotations

from fastui import AnyComponent
from fastui import components as c
from fastui.events import GoToEvent


def base_page(
    *components: AnyComponent, title: str | None = None
) -> list[AnyComponent]:
    return [
        c.PageTitle(text="AHP"),
        c.Navbar(
            title="AHP",
            title_event=GoToEvent(url="/materials"),
            start_links=[
                c.Link(
                    components=[c.Text(text="Теория")],
                    on_click=GoToEvent(url="/materials"),
                    active="startswith:/materials",
                ),
                c.Link(
                    components=[c.Text(text="Калькулятор")],
                    on_click=GoToEvent(url="/caclulator"),
                    active="startswith:/calclulator",
                ),
            ],
        ),
        c.Page(
            components=[
                # *((c.Heading(text=title),) if title else ()),
                *components,
            ],
        ),
        c.Footer(
            extra_text="Квартовкин Святослав",
            links=[
                c.Link(
                    components=[c.Text(text="Github")],
                    on_click=GoToEvent(url="https://github.com/margorsq"),
                ),
            ],
        ),
    ]
