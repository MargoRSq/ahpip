from fastapi import APIRouter
from fastui import FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from pydantic import BaseModel

from src.pages.shared import base_page

router = APIRouter()


class CompareElement(BaseModel):
    desc: str = ''
    value: str


compare_elements_dict = {
    '1/9': 'Принципиально хуже',
    '1/8': '',
    '1/7': 'Значительно хуже',
    '1/6': '',
    '1/5': 'Хуже',
    '1/4': '',
    '1/3': 'Немного хуже',
    '1/2': '',
    '1': 'Равная важность',
    '2': '',
    '3': 'Немного лучше',
    '4': '',
    '5': 'Лучше',
    '6': '',
    '7': 'Значительно лучше',
    '8': '',
    '9': 'Принципиально лучше',
}

compare_elements = [
    CompareElement(desc=key, value=value)
    for key, value in compare_elements_dict.items()
]
instruction = [
    c.Markdown(
        text="""### Инструкция
1. Откройте вкладку **Калькулятор** в меню сверху
2. Прикрепите **json файл**, содержащий критерии и объекты сравнения для метода анализа иерархий
Пример файла:
```json
{
"criterias": [
    "Ёмкость сети",
    "Энергопотребление передатчика",
    "Пропускная способность канала",
    "Стоимость радиомодуля",
    "Радиус действия базовой станции"
	],
"objects": [
    "NB-IoT",
    "LoRa",
    "Стриж",
    "URLLC"
	]
}
```
2. Заполнить страницу попарных сравнений критериев и объектов по критериям используя **шкалу относительности**.""",
    ),
    c.Table(
        data=compare_elements,
        columns=[
            DisplayLookup(
                field='value', title='Присваиваемая оценка', mode=DisplayMode.plain
            ),
            DisplayLookup(
                field='desc',
                title='Результат субъективного сравнения',
                mode=DisplayMode.plain,
            ),
        ],
    ),
    c.Markdown(
        text='3. Сохранить получившиеся результаты себе на компьютер удобным методом'
    ),
]


@router.get('/instruction', response_model=FastUI, response_model_exclude_none=True)
def materials():
    return base_page(*instruction)
