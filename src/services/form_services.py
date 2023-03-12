from typing import List

from aiogram import types

from config import config
from misc import bot
from utils import consts
from db.models import Question, QuestionForm, QuestionFormWithQuestion


async def get_question(question_id):
    question = await Question.get_or_none(id=question_id)
    if question:
        title = question.title

        return title


def format_message(form_id, items: dict):
    s = [f'<b>Номер анкеты</b>: #{form_id}<br>']
    for k, v in items.items():
        s.append(f'<b>{k}</b>: {v}<br>')
    return ''.join(s)


async def form_send(form_id, questions: List[dict]):
    to_db = []

    for question in questions:
        idx, value = list(question.items())[0]
        obj = QuestionFormWithQuestion(question_form_id=form_id, question_id=idx, answer=value)
        to_db.append(obj)

    await QuestionFormWithQuestion.bulk_create(to_db)

    await form_channel_send(form_id)
    await form_channel_admin_send(form_id)


async def form_channel_send(form_id):
    questions = await QuestionFormWithQuestion.filter(question_form_id=form_id, question__is_admin_only=False,
                                                      answer__isnull=False) \
        .select_related('question') \
        .order_by('question_id')
    items = {}
    for question in questions:
        items[question.question.title] = question.answer

    await bot.send_message(config.CHANNEL_ID, format_message(form_id, items), parse_mode='HTML')


async def form_channel_admin_send(form_id):
    questions = await QuestionFormWithQuestion.filter(question_form_id=form_id, question__is_admin_only=True,
                                                      answer__isnull=False) \
        .select_related('question') \
        .order_by('question_id')
    items = {}
    for question in questions:
        items[question.question.title] = question.answer

    await bot.send_message(config.CHANNEL_ADMIN_ID, format_message(form_id, items), parse_mode='HTML')


def start_keyboard():
    kb = [
        [types.KeyboardButton(text=consts.SKIP)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    return keyboard


def middle_keyboard():
    kb = [
        [types.KeyboardButton(text=consts.SKIP)],
        [types.KeyboardButton(text=consts.BACK)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    return keyboard


def end_keyboard():
    kb = [
        [types.KeyboardButton(text=consts.BACK)],
        [types.KeyboardButton(text=consts.COMPLETE)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    return keyboard
