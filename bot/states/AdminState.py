from aiogram.fsm.state import StatesGroup, State


class UserAccessStates(StatesGroup):
    waiting_for_add_user = State()
    waiting_for_delete_user = State()
