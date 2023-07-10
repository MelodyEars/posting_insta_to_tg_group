from aiogram import types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from loguru import logger

from TG_bot.src.telegram.buttons.user_btn import one_btn
from TG_bot.src.telegram.handlers.fsm_h.download_by_link import TikTokOneVideo
from TG_bot.src.telegram.handlers.user_handlers.callback_autoposing import user_router
from TG_bot.src.telegram.messages.user_msg import DownloadByLinkMessages, MESSAGES


@user_router.callback_query(Text("download_by_link_tt"))
async def download_tt_video_by_link(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    logger.info(f"to have callback")

    await state.set_state(TikTokOneVideo.link)
    await message.reply(DownloadByLinkMessages['enter_link'], reply_markup=one_btn(MESSAGES['back']))
