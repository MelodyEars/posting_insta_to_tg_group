from aiogram.types import Message
from loguru import logger

from TG_bot.src.telegram.buttons.user_btn import many_btns
from TG_bot.src.telegram.messages.user_msg import MESSAGES, ErrorMessages
from database.query.set_up_social_network import db_chanels_by_id_chat


async def watch_connection_channels(message: Message):
    tg_username = message.from_user.username
    logger.info(f"request {tg_username} to watch their channels")

    chat_id = message.chat.id
    tt_chanel, tg_chanel = db_chanels_by_id_chat(chat_id)
    if tt_chanel and tg_chanel:
        logger.info(f'{tg_username} tg = {tg_chanel} and tt = {tt_chanel}' )
        msg = f"""
                TikTok: https://vm.tiktok.com/@{tt_chanel} ➡️ Telegram: {tg_chanel}  
               """
    else:
        logger.error(f"{tg_username} not registration their channels")
        msg = ErrorMessages['request_attend_settings']

    await message.reply(
                msg,
                reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                                       txt_input_field=MESSAGES['main_input_field'])
            )
