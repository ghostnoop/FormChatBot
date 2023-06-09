from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from db.models import QuestionForm
from services import form_services
from services.form_services import form_send
from states.FormStates import FormStates
from utils import consts

router = Router()


@router.message(FormStates.middle, F.text == consts.BACK)
async def back_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_id = data['question_current_id']
    t = data['questions'].pop()
    current_id -= 2
    data['question_current_id'] = current_id
    await state.update_data(data)
    await answer_form(message, state, back=True)


@router.message(FormStates.middle, F.text == consts.SKIP)
async def skip_handler(message: types.Message, state: FSMContext):
    await answer_form(message, state, skip=True)


@router.message(Command("form"))
async def create_form_start(message: types.Message, state: FSMContext):
    text = f'Создание анкеты'
    await message.answer(text)

    question, _ = await form_services.get_question(1)
    if question:
        await message.answer(question, reply_markup=form_services.start_keyboard())

    form, _ = await QuestionForm.get_or_create(user_id=message.from_user.id, is_done=False)

    await state.set_state(FormStates.start)
    await state.update_data({'form_id': form.id, 'question_current_id': 1, 'questions': []})


@router.message(FormStates.start, F.text)
@router.message(FormStates.middle, F.text)
async def answer_form(message: types.Message, state: FSMContext, skip=False, back=False):
    data = await state.get_data()
    current_id = data['question_current_id']

    if skip:
        text = None
    else:
        text = message.text
    if not back:
        data['questions'].append({current_id: text})
    current_id += 1

    data['question_current_id'] = current_id

    await state.update_data(data)

    question, kb = await form_services.get_question(current_id)
    if question:
        await state.set_state(FormStates.middle)
        kb = kb if kb else form_services.middle_keyboard()

        await message.answer(question, reply_markup=kb)
    else:
        await state.set_state(FormStates.end)
        await message.answer('Вопросы закончились', reply_markup=form_services.end_keyboard())


@router.message(FormStates.end, F.text == consts.COMPLETE)
async def complete_form(message: types.Message, state: FSMContext):
    data = await state.get_data()

    questions = data['questions']
    form_id = data['form_id']
    await form_send(form_id, questions)

    await state.clear()

    form = await QuestionForm.get(id=form_id)
    form.is_done = True
    await form.save()
    await message.answer(consts.COMPLETE_MESSAGE, reply_markup=types.ReplyKeyboardRemove())
    {"не был женат","не была замужем", "разведён", "разведена"}
