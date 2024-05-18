from fastui.forms import SelectOption
from pydantic import BaseModel

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


class CompareElement(BaseModel):
    desc: str = ''
    value: str


compare_elements = [
    CompareElement(desc=key, value=value)
    for key, value in compare_elements_dict.items()
]

enum_selector = [SelectOption(label=key, value=key) for key in compare_elements_dict]

about_markdown_str = """# Метод анализа иерархий

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

instruction_start_markdown_str = """### Инструкция
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
**ИЛИ** уже заранее заполненные попарные сравнения в **строгой** последовательности
(пример к предыдущим критериям и объектам)
```json
{
    "criteria": {
        "Ёмкость сети": {
            "Энергопотребление передатчика": "5",
            "Пропускная способность канала": "6",
            "Стоимость радиомодуля": "6",
            "Радиус действия базовой станции": "1"
        },
        "Энергопотребление передатчика": {
            "Пропускная способность канала": "1/ 5",
            "Стоимость радиомодуля": "5",
            "Радиус действия базовой станции": "2"
        },
        "Пропускная способность канала": {
            "Стоимость радиомодуля": "3",
            "Радиус действия базовой станции": "1 / 7"
        },
        "Стоимость радиомодуля": {
            "Радиус действия базовой станции": "1 / 3"
        }
    },
    "object": {
        "Ёмкость сети": {
            "NB-IoT и LoRa": "5",
            "NB-IoT и Стриж": "6",
            "NB-IoT и URLLC": "1 / 3",
            "LoRa и Стриж": "1 / 2",
            "LoRa и URLLC": "1 / 5",
            "Стриж и URLLC": "1 / 5"
        },
        "Энергопотребление передатчика": {
            "NB-IoT и LoRa": "1 / 5",
            "NB-IoT и Стриж": "1 / 6",
            "NB-IoT и URLLC": "3",
            "LoRa и Стриж": "1 / 2",
            "LoRa и URLLC": "5",
            "Стриж и URLLC": "6"
        },
        "Пропускная способность канала": {
            "NB-IoT и LoRa": "5",
            "NB-IoT и Стриж": "9",
            "NB-IoT и URLLC": "1 / 3",
            "LoRa и Стриж": "6",
            "LoRa и URLLC": "1 /6",
            "Стриж и URLLC": "1 / 8"
        },
        "Стоимость радиомодуля": {
            "NB-IoT и LoRa": "3",
            "NB-IoT и Стриж": "1 / 3",
            "NB-IoT и URLLC": "3",
            "LoRa и Стриж": "1 / 6",
            "LoRa и URLLC": "4",
            "Стриж и URLLC": "5"
        },
        "Радиус действия базовой станции": {
            "NB-IoT и LoRa": "2",
            "NB-IoT и Стриж": "3",
            "NB-IoT и URLLC": "4",
            "LoRa и Стриж": "1 / 3",
            "LoRa и URLLC": "8",
            "Стриж и URLLC": "9"
        }
    }
}
```
3. Заполнить страницу попарных сравнений критериев и объектов по критериям используя **шкалу относительности**."""  # noqa: E501

instruction_end_markdown_str = (
    '4. Сохранить получившиеся результаты себе на компьютер удобным методом'  # noqa: E501
)
