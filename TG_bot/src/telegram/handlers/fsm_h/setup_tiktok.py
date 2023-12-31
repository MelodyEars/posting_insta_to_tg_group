from typing import NamedTuple

from loguru import logger

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from TG_bot.setup import user_router
from TG_bot.src.telegram.buttons.user_btn import many_btns
from TG_bot.src.telegram.messages.user_msg import MESSAGES, SetUpTikTokMessages
from database.query.set_up_social_network import db_create_TT_user


class SetUpTikTok(StatesGroup):
    tiktok_login = State()


class StructData(NamedTuple):
    tiktok_login: str


@user_router.message(F.text == MESSAGES['back'])
async def cancel_handler(message: Message, state: FSMContext, text=''):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    if text:
        await message.reply(
            text,
            reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                                   txt_input_field=MESSAGES['settings_input_field'])
        )

    else:
        await message.answer(
            text=message.text,
            reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                                   txt_input_field=MESSAGES['settings_input_field'])
        )


@user_router.message(SetUpTikTok.tiktok_login)
async def answer_login(message: Message, state: FSMContext):
    logger.info("message.text: " + message.text)
    logger.info("owner: " + message.from_user.username)

    msg_text = message.text.replace("\n", "").replace(" ", "").replace("@", "")
    if msg_text == "":
        # if empty request
        await cancel_handler(message, state, MESSAGES['empty_request'])
        return

    await state.update_data(tiktok_login=message.text)
    data = await state.get_data()
    struct_data = StructData(**data)

    # Add to DB
    id_chat_user = message.chat.id
    new_login_tt = struct_data.tiktok_login
    db_create_TT_user(tt_username=new_login_tt, id_chat_user=id_chat_user)

    await state.clear()
    await message.reply(
        SetUpTikTokMessages['success_tt'],
        reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                               txt_input_field=MESSAGES['settings_input_field'])
    )
