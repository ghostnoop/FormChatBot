from aiogram.fsm.state import StatesGroup, State


class FormStates(StatesGroup):
    start = State()
    middle = State()
    end = State()
