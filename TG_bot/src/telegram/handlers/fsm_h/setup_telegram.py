
from typing import NamedTuple

from loguru import logger

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from TG_bot.setup import user_router
from TG_bot.src.telegram.buttons.user_btn import one_btn, many_btns
from TG_bot.src.telegram.messages.user_msg import MESSAGES, SetUpTelegramMessages


class SetUpTelegram(StatesGroup):
    api_id = State()
    api_hash = State()


class StructData(NamedTuple):
    api_id: str
    api_hash: str


@user_router.message(F.text == MESSAGES['back'])
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.reply(
        'ㅤ',
        reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                               txt_input_field=MESSAGES['settings_input_field'])
    )


@user_router.message(SetUpTelegram.api_id)
async def answer_login(message: Message, state: FSMContext):
    await state.set_state(SetUpTelegram.api_hash)
    await state.update_data(api_id=message.text)

    await message.reply(SetUpTelegramMessages['quest_telegram_id'], reply_markup=one_btn(MESSAGES['back']))


@user_router.message(SetUpTelegram.api_hash)
async def answer_password(message: Message, state: FSMContext):
    await state.update_data(api_hash=message.text)

    data = await state.get_data()
    struct_data = StructData(**data)

    logger.info(struct_data.api_id)
    logger.info(struct_data.api_hash)

    await state.clear()
    await message.reply(
        SetUpTelegramMessages['success'],
        reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                               txt_input_field=MESSAGES['settings_input_field'])
    )
