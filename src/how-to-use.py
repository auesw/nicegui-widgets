from nicegui import ui, app
from pathlib import Path

from widgets.country_dropdown_selection import DropdownCountryFlagsWidget
from widgets.currency import CurrencyWidget

app.add_static_files('/static', Path(__file__).parent.parent / 'static')

# Country dropdown selection
DropdownCountryFlagsWidget(text='', auto_close=True)

# CurrencyWidget
CurrencyWidget()

ui.run(language='pt-BR', title='Gerenciador de finanças', favicon='https://cdn-icons-png.flaticon.com/512/3135/3135715.png', dark=True)
