import asyncio

from aiogram import types
from aiogram.filters import Text
from loguru import logger

from TG_bot.setup import dp
from TG_bot.src.telegram.buttons.user_btn import one_inline_btn
from TG_bot.src.telegram.handlers.btn_task_main_menu import autoposting_tt_inline_btn_task, \
    stop_autoposting_tt_inline_btn_task
from TG_bot.src.telegram.messages.user_msg import ProcessActions

from database.query.btns_main_menu import db_get_tt_name_by_tg_id
from database.query.users import get_user_by_tg_id
from database.tables import TikTokUser


@dp.callback_query(Text("start_tt_auto"))
async def run_autoposting(callback: types.CallbackQuery):
    logger.info("start_tt_auto")
    message = callback.message
    obj_tiktok_user: TikTokUser = db_get_tt_name_by_tg_id(message.from_user.id)
    group_chat_id = get_user_by_tg_id(message.from_user.id).group_chat_id

    autoposting = asyncio.create_task(autoposting_tt_inline_btn_task(message, obj_tiktok_user, group_chat_id))
    builder = one_inline_btn("Turn OFF autoposting", "end_tt_auto")
    await message.edit_text("Process was activated.", reply_markup=builder.as_markup())

    await autoposting


@dp.callback_query(Text("end_tt_auto"))
async def end_posting(callback: types.CallbackQuery):
    message = callback.message

    end_autoposting = asyncio.create_task(stop_autoposting_tt_inline_btn_task(message))
    builder = one_inline_btn("Run autoposting", "start_tt_auto")
    await message.edit_text(ProcessActions['stop_autoposting'], reply_markup=builder.as_markup())

    await end_autoposting
