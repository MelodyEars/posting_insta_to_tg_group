
from typing import NamedTuple

from loguru import logger

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from TG_bot.setup import user_router
from TG_bot.src.telegram.buttons.user_btn import one_btn, many_btns
from TG_bot.src.telegram.messages.user_msg import MESSAGES, SetUpInstaMessages


class SetUpInstagram(StatesGroup):
    insta_login = State()
    insta_password = State()


class StructData(NamedTuple):
    insta_login: str
    insta_password: str


@user_router.message(F.text == MESSAGES['back'])
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.reply(
        '',
        reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                               txt_input_field=MESSAGES['settings_input_field'])
    )


@user_router.message(SetUpInstagram.insta_login)
async def answer_login(message: Message, state: FSMContext):
    await state.set_state(SetUpInstagram.insta_password)
    await state.update_data(insta_login=message.text)

    await message.reply(SetUpInstaMessages['quest_insta_password'], reply_markup=one_btn(MESSAGES['back']))


@user_router.message(SetUpInstagram.insta_password)
async def answer_password(message: Message, state: FSMContext):
    await state.update_data(insta_password=message.text)
    await state.clear()

    data = await state.get_data()
    struct_data = StructData(**data)

    logger.info(struct_data.insta_login)
    logger.info(struct_data.insta_password)

    await message.reply(
        SetUpInstaMessages['success'],
        reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                               txt_input_field=MESSAGES['settings_input_field'])
    )
