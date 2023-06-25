from typing import NamedTuple

from loguru import logger

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from TG_bot.setup import user_router
from TG_bot.src.telegram.buttons.user_btn import one_btn, many_btns
from TG_bot.src.telegram.messages.user_msg import MESSAGES, SetUpTikTokMessages


class SetUpTikTok(StatesGroup):
    tiktok_login = State()
    tiktok_password = State()


class StructData(NamedTuple):
    tiktok_login: str
    tiktok_password: str


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


@user_router.message(SetUpTikTok.tiktok_login)
async def answer_login(message: Message, state: FSMContext):
    await state.set_state(SetUpTikTok.tiktok_password)
    await state.update_data(tiktok_login=message.text)

    await message.reply(SetUpTikTokMessages['quest_tiktok_password'], reply_markup=one_btn(MESSAGES['back']))


@user_router.message(SetUpTikTok.tiktok_password)
async def answer_password(message: Message, state: FSMContext):
    await state.update_data(tiktok_password=message.text)
    await state.clear()

    data = await state.get_data()
    struct_data = StructData(**data)

    logger.info(struct_data.tiktok_login)
    logger.info(struct_data.tiktok_password)

    await message.reply(
        SetUpTikTokMessages['success'],
        reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                               txt_input_field=MESSAGES['settings_input_field'])
    )
