from nicegui import ui
from nicegui.elements.input import Input
from nicegui.events import ValueChangeEventArguments

from ..country_dropdown_selection.dropdown_flag import DropdownCountryFlagsWidget
from ..country_dropdown_selection.country_api import Country

class CurrencyWidget(ui.element):
    def __init__(self, label: str = 'Label'):
        self._amount: float = 0.0
        self._country_dropdown: DropdownCountryFlagsWidget
        self._input: Input

        
        self._is_formatting_input: bool = False
        """
        Determines whether this widget is currently formatting an input or not

        This boolean is necessary so that the on_value_change callback doesn't
        enter in an infinite loop
        """

        with ui.row():
            self._country_dropdown = DropdownCountryFlagsWidget(text='', auto_close=True)

            self._input = Input(
                label=label,
                placeholder="0,00",
                value="0,00",
                prefix=self.selected_country.currency_symbol
            )
            self._input.props('outlined dense')
            self._input.on_value_change(callback=self._on_input_change)
            self._input.on(type='keydown.enter', handler=self._on_input_enter)
            self._input.on(type='focus', handler=self._on_input_focus)

        self._country_dropdown.on_value_change(callback=self._on_country_change)

    def _on_country_change(self, e: ValueChangeEventArguments) -> None:
        self._input.prefix = self.selected_country.currency_symbol

    def _on_input_change(self, e: ValueChangeEventArguments) -> None:
        if self._is_formatting_input: return
        self._is_formatting_input = True

        value_no_separator: str = e.value.replace(',', '')
        new_input: str = e.value
    
        try:
            if len(value_no_separator) <= 3:
                new_input = f'0,{value_no_separator.lstrip('0')}'            
            else:
                new_input = f'{value_no_separator[:-2]},{value_no_separator[-2:]}'
                new_input = new_input.lstrip('0')

            self._input.value = new_input
            self._input.update()
        finally:
            self._is_formatting_input = False

    def _on_input_enter(self) -> None:
        self.amount = self._input.value
        ui.notify(f'{self._input.prefix} {self._input.value}')

    def _on_input_focus(self) -> None:
        self._input.run_method('select')

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value: float | int) -> None:
        if isinstance(value, int):
            self._amount = float(value)
        else:
            self._amount = value
    
    @property
    def selected_country(self) -> Country:
        """No need for a setter. This is done in the DropdownCountryFlagsWidget"""
        return self._country_dropdown.selected_country
