from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, Row, Back, Select, ScrollingGroup
from aiogram import Router
from aiogram.filters.state import State, StatesGroup
from typing import Any
from aiogram.types import CallbackQuery
import operator

rt = Router()

class ViewPassStates(StatesGroup):
    select_pass = State()
    view_pass_info = State()

SCROLLING_HEIGHT = 6

async def get_passwords(dialog_manager: DialogManager, **middleware_data):
    
    

    data = {
        'passwords': [
            ('GitHub', 'pidoras@gmail.com', 'asfsaf', 10),
            ('Gmail' , 'guesos@gmail.com','xzasfasfx' , 20)
        ]
    }
    return data
async def get_pass_info(dialog_manager: DialogManager, **middleware_data):
    #session = middleware_data.get('session')
    context = dialog_manager.current_context()
    pass_id = int(context.dialog_data['pass_id'])

    data = {
        'pass_id': pass_id,
    }
    return data

async def on_chosen_pass(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(pass_id=item_id)
    
    await manager.switch_to(ViewPassStates.view_pass_info)

def get_scrolling_group(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[0]}" + ":" + "{item[1]}"),
            id="s_scroll_pass",
            item_id_getter=operator.itemgetter(3),
            items="passwords",
            on_click=on_click,
        ),
        id="pass_ids",
        width=1, height=SCROLLING_HEIGHT,
    )
def get_passwords_window():
    return Window(
        Const('Choose pass:'),
        get_scrolling_group(on_chosen_pass),
        Cancel(Const('<-- Close -->')),
        state=ViewPassStates.select_pass,
        getter=get_passwords
    )
def get_pass_info_window():
    return Window(
        Format(
'''
Name: {pass_id}
Login:
Password: 
'''
        ),
        Button(Const("⚙️ Изменить имя"), id="change_name"),
        Button(Const("⚙️ Изменить логин"), id="change_login"),
        Button(Const("⚙️ Изменить пароль"), id="change_pass"),
        Back(Const('<< Назад')),
        Cancel(Const("<-- Закрыть -->")),
        getter=get_pass_info,
        state=ViewPassStates.view_pass_info
    )

rt.include_router(Dialog(get_passwords_window(), get_pass_info_window()))