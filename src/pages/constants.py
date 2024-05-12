from fastui.forms import SelectOption

enum_values = {
    'one_nine': '1 / 9',
    'one_eight': '1 / 8',
    'one_seven': '1 / 7',
    'one_six': '1 / 6',
    'one_five': '1 / 5',
    'one_four': '1 / 4',
    'one_three': '1 / 3',
    'one_twop': '1 / 2',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

enum_selector = [
    SelectOption(label=value, value=value) for key, value in enum_values.items()
]
