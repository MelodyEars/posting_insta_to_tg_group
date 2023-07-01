import asyncio
from contextlib import suppress

from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Text
from loguru import logger

from TG_bot.src.telegram.buttons.user_btn import one_inline_btn
from TG_bot.src.telegram.handlers.btn_task_main_menu import autoposting_tt_inline_btn_task, \
    stop_autoposting_tt_inline_btn_task
from TG_bot.src.telegram.messages.user_msg import ProcessActions
from TG_bot.src.telegram.handlers.user_handlers import user_router


from database.query.btns_main_menu import db_get_tt_name_by_tg_id
from database.query.users import get_user_by_tg_id
from database.tables import TikTokUser


@user_router.callback_query(Text("start_tt_auto"))
async def run_autoposting(callback: types.CallbackQuery):
    logger.info("start_tt_auto")
    message = callback.message

    obj_tiktok_user: TikTokUser = db_get_tt_name_by_tg_id(message.chat.id)
    group_chat_id = get_user_by_tg_id(message.chat.id).group_chat_id

    autoposting = asyncio.create_task(autoposting_tt_inline_btn_task(message, obj_tiktok_user, group_chat_id))

    builder = one_inline_btn("Turn OFF autoposting", "end_tt_auto")
    with suppress(TelegramBadRequest):
        await message.edit_text("Process was activated.", reply_markup=builder.as_markup())
    await callback.answer()

    await autoposting


@user_router.callback_query(Text("end_tt_auto"))
async def end_posting(callback: types.CallbackQuery):
    message = callback.message

    end_autoposting = asyncio.create_task(stop_autoposting_tt_inline_btn_task(message))
    builder = one_inline_btn("Run autoposting", "start_tt_auto")

    with suppress(TelegramBadRequest):
        await message.edit_text(ProcessActions['stop_autoposting'], reply_markup=builder.as_markup())

    await callback.answer()
    await end_autoposting
