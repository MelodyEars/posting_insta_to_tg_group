import asyncio

from aiogram import types
from aiogram.filters import Text

from TG_bot.setup import dp
from TG_bot.src.telegram.handlers.btn_task_main_menu import autoposting_tt_inline_btn_task, \
    stop_autoposting_tt_inline_btn_task
from TG_bot.src.telegram.messages.user_msg import ProcessActions
from database.query.btns_main_menu import db_get_tt_name_by_tg_id
from database.query.users import get_user_by_tg_id
from database.tables import TikTokUser


@dp.callback_query(Text("start_tt_auto"))
async def run_autoposting(callback: types.CallbackQuery):
    message = callback.message
    obj_tiktok_user: TikTokUser = db_get_tt_name_by_tg_id(message.from_user.id)
    group_chat_id = get_user_by_tg_id(message.from_user.id).group_chat_id

    await message.answer(ProcessActions['start_autoposting'], )

    autoposting = asyncio.create_task(autoposting_tt_inline_btn_task(message, obj_tiktok_user, group_chat_id))
    await autoposting


@dp.callback_query(Text("start_tt_auto"))
async def end_posting(callback: types.CallbackQuery):
    message = callback.message

    end_autoposting = asyncio.create_task(stop_autoposting_tt_inline_btn_task(message))
    await end_autoposting


