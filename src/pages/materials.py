from fastapi import APIRouter
from fastui import FastUI
from fastui import components as c
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

about_ahp = [
    c.Markdown(
        text="""# Метод анализа иерархий

### История и суть

В 1970 г. Томас Саати (США) разработал метод анализа иерархий - **Analityc hierarchy process (AHP)**. Относится к классу критериальных методов. Получил широкое распространение и до сих пор активно используется в управленческой практике. Приводит ЛПР не к «правильному» решению, а к варианту, наилучшим образом согласующемуся с его пониманием сути проблемы и требованиями к ее решению.

### Этапы метода

1. Выделение проблемы. Определение цели.
2. Выделение основных критериев и альтернатив. 
3. Построение иерархии: дерево от цели через критерии к альтернативам.
4. Построение матрицы попарных сравнений критериев по цели и альтернатив по критериям. **(выполняется программой)**
5. Применение методики анализа полученных матриц. **(выполняется программой)**
6. Определение весов альтернатив по системе иерархии. **(выполняется программой)**

"""  # noqa: E501
    ),
    c.Image(src='/static/ahp_tree.jpeg'),
]


@router.get('/theory', response_model=FastUI, response_model_exclude_none=True)
def materials():
    return base_page(*about_ahp)
