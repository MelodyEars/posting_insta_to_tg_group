
from typing import NamedTuple

from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, Chat
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from TG_bot.setup import user_router, bot
from TG_bot.src.telegram.buttons.user_btn import many_btns
from TG_bot.src.telegram.messages.user_msg import MESSAGES, SetUpTelegramMessages
from database.query.set_up_social_network import db_add_tg_groupname


class SetUpTelegram(StatesGroup):
    link_your_chanel = State()


class StructData(NamedTuple):
    link_your_chanel: str


@user_router.message(F.text == MESSAGES['back'])
async def cancel_handler(message: Message, state: FSMContext, text='ㅤ'):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.reply(
        text,
        reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                               txt_input_field=MESSAGES['settings_input_field'])
    )


@user_router.message(SetUpTelegram.link_your_chanel)
async def answer_login(message: Message, state: FSMContext):
    msg_text = message.text.replace("\n", "").replace(" ", "")
    if msg_text == "":
        # if empty request
        await cancel_handler(message, state, MESSAGES['empty_request'])
        return

    await state.set_state(SetUpTelegram.link_your_chanel)
    await state.update_data(link_your_chanel=msg_text)

    data = await state.get_data()
    struct_data = StructData(**data)

    link_your_chanel = struct_data.link_your_chanel

    try:
        result: Chat = await bot.get_chat(link_your_chanel)
        print(f"Result {result}")
        chat_id = result.id
        print(f"Chat id {chat_id}")

        db_add_tg_groupname(group_chat_id=chat_id, id_telegram=message.from_user.id)

    except TelegramBadRequest:
        await cancel_handler(message, state, SetUpTelegramMessages['send_username'])

    await cancel_handler(message, state, SetUpTelegramMessages['success'])
