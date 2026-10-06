from nicegui import ui, app
from nicegui.elements.input import Input
from pathlib import Path
from widgets.currency.currency import CurrencyWidget

app.add_static_files('/static', Path(__file__).parent.parent / 'static')

CurrencyWidget()

ui.run(language='pt-BR', title='Gerenciador de finanças', favicon='https://cdn-icons-png.flaticon.com/512/3135/3135715.png', dark=True)


