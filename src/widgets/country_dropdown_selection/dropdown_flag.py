import nicegui
from nicegui import ui, app
from nicegui.events import ValueChangeEventArguments
from pathlib import Path
from dataclasses import dataclass
from .country_api import CountryApiWrapper, Country
from typing import List
PROJECT_ROOT_FOLDER = Path(__file__).resolve().parent.parent.parent
locale = 'pt_BR'

#app.add_static_files('/static', PROJECT_ROOT_FOLDER / 'static')

currencies = {
    'brazil':   {'label': 'BR', 'image': 'static/BR.svg', 'value': 'R$'},
    'usa':      {'label': 'US', 'image': 'static/US.svg', 'value': 'US$'}
}

class DropdownCountryFlagsWidget(ui.dropdown_button):
    def __init__(self, **kwargs) -> None:
        super().__init__(kwargs)
        self._api = CountryApiWrapper()
        #self._countries> List[Country] = self._api.get_all_countries()
        self._countries: List[Country] = []
        self._countries.append(self._api.get_country_by_name('brazil'))
        self._countries.append(self._api.get_country_by_name('united states of america'))

        with self as btn:
            btn.set_text(kwargs['text'])
            if kwargs['auto_close']: btn.props('auto-close')
            btn.set_icon(f'img:{self._countries[0][0].flag}')
            btn.props('flat content-class="transparent-menu"')

            for country in self._countries:
                with ui.item(on_click=lambda c=country[0]: btn._on_item_click(c)):
                    with ui.item_section().props('avatar'):
                        ui.image(country[0].flag).classes('w-7 h-4.5')
                    with ui.item_section():
                        ui.item_label(country[0].alpha2_code)

        self._selected_country: Country = self._countries[0][0]
        #self._on_item_click(self._countries[0][0], show_name=False)
        self._api.close()

    @property
    def selected_country(self) -> Country:
        return self._selected_country

    @selected_country.setter
    def selected_country(self, value: Country) -> None:
        self._selected_country = value

    @property
    def countries(self) -> List[Country]:
        return self._countries

    @countries.setter
    def countries(self, value: List[Country]) -> None:
        self._countries = value
    def _on_item_click(self, country: Country, show_name=False) -> None:
        #self.set_icon(f'img:static/{self.country.alpha2_code}.svg')
        self.set_icon(f'img:{country.flag}')
        if show_name: self.set_text(country.alpha2_code)
        else: self.set_text=''
        self.selected_country = country



"""
def set_dropdown_icon(selection: dict) -> None:
    btn.set_icon(f'img:{currencies[selection]['image']}')

with ui.dropdown_button('', auto_close=True) as btn:
    btn.set_icon(f'img:{currencies['brazil']['image']}')
    btn.props('flat content-class="transparent-menu"')
    for curr in currencies:
        with ui.item(on_click=lambda c=curr: set_dropdown_icon(c)):
            with ui.item_section().props('avatar'):
                ui.image(currencies[curr]['image']).classes('w-6 h-6')
            with ui.item_section():
                ui.item_label(currencies[curr]['label'])
"""