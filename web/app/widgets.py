from django.forms.widgets import NumberInput, RadioSelect


class RangeInput(NumberInput):
    input_type = 'range'

