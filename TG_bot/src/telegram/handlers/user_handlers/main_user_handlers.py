
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from loguru import logger

from TG_bot.src.telegram.handlers.fsm_h.download_by_link import user_router
from TG_bot.src.telegram.buttons.user_btn import one_btn, many_btns
from TG_bot.src.telegram.handlers.fsm_h.setup_telegram import SetUpTelegram
from TG_bot.src.telegram.handlers.fsm_h.setup_tiktok import SetUpTikTok
from TG_bot.src.telegram.handlers.user_handlers.act_by_hanler.watcher_chanels import watch_connection_channels
from TG_bot.src.telegram.handlers.user_handlers.callbacks.callback_autoposing import run_autoposting, end_posting
from TG_bot.src.telegram.handlers.user_handlers.callbacks.callback_donload_by_link import download_tt_video_by_link
from TG_bot.src.telegram.messages.user_msg import (MESSAGES, SetUpTikTokMessages, SetUpTelegramMessages,
                                                   ErrorMessages)
from database.query.btns_main_menu import db_get_tt_name_by_tg_id
from database.query.registration import db_add_user
from database.query.users import get_user_by_tg_id

from database.tables import TikTokUser


@user_router.message(Command(commands='start'))
async def start(message: Message):
    db_add_user(chat_id_user=message.chat.id, tg_username=message.from_user.username)

    await message.reply(
        MESSAGES['start_message'],
        reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                               txt_input_field=MESSAGES['main_input_field'])
    )


@user_router.message(Command(commands='help'))
async def helper(message: Message):
    await message.reply(
        MESSAGES['help'],
        reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                               txt_input_field=MESSAGES['main_input_field'])
    )


@user_router.message(F.text == MESSAGES['back'])
async def back_handl(message: Message):
    await message.answer(
        text=message.text,
        reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                               txt_input_field=MESSAGES['main_input_field'])
    )


@user_router.message(F.text.in_(MESSAGES['main_btn_list']))
async def starter_work(message: Message, state: FSMContext):
    logger.info("starter_work")
    # _______________________________________________________________________________   TikTok
    if message.text == MESSAGES['main_btn_list'][0]:
        # TODO tiktokapi not have video on tiktok page
        logger.info(f"TikTok {message.from_user.username}")
        obj_tiktok_user: TikTokUser = db_get_tt_name_by_tg_id(message.chat.id)
        group_chat_id = get_user_by_tg_id(message.chat.id).group_chat_id

        if not (obj_tiktok_user is None and group_chat_id is None):
            if not obj_tiktok_user.autoposting_tt:
                # still not run autoposting
                logger.info("still not run autoposting")
                await run_autoposting(message)
                # list_btns = ["🔄 Run autoposting", "📥 Download by link"]
                # list_callback = ["start_tt_auto", "download_by_link_tt"]

            else:
                # already run autoposting
                logger.info("already run autoposting")
                # list_btns = ["❌ Turn OFF autoposting", "📥 Download by link"]
                # list_callback = ["end_tt_auto", "download_by_link_tt"]
                await end_posting(message)

            # builder = many_inline_btns(list_btns, list_callback)
            # await message.answer(ProcessActions["msg_start_autoposting"], reply_markup=builder.as_markup())

        else:
            await message.answer(ErrorMessages['request_attend_settings'] + 'Tiktok')
            # Todo add inline-button for setup tiktok and telegram

    # _______________________________________________________________________________  Download by link
    elif message.text == MESSAGES['main_btn_list'][1]:
        # builder = one_inline_btn("TikTok", "download_by_link_tt")
        # await message.answer(message.text, reply_markup=builder.as_markup())
        await download_tt_video_by_link(message, state)

    # _______________________________________________________________________________  Settings
    elif message.text == MESSAGES['main_btn_list'][2]:
        logger.info(f"Setting {message.from_user.username}")
        await message.answer(
            text=message.text,
            reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                                   txt_input_field=MESSAGES['settings_input_field'])
        )


@user_router.message(F.text.in_(MESSAGES['settings_btn_list']))
async def setup_social_network(message: Message,  state: FSMContext):
    if message.text == MESSAGES['settings_btn_list'][0]:  # SetUP TikTok
        await state.set_state(SetUpTikTok.tiktok_login)
        await message.reply(SetUpTikTokMessages['quest_tiktok_login'], reply_markup=one_btn(MESSAGES['back']))

    elif message.text == MESSAGES['settings_btn_list'][1]:  # SetUP Telegram
        await state.set_state(SetUpTelegram.link_your_chanel)
        await message.reply(SetUpTelegramMessages['nickname_chanel'], reply_markup=one_btn(MESSAGES['back']))

    elif message.text == MESSAGES['settings_btn_list'][2]:  # settings_btn_list
        await watch_connection_channels(message)

    elif message.text == MESSAGES['settings_btn_list'][3]:  # Support
        await message.answer(
            'Contact us: \n https://t.me/+mbJKlsjGfmE5ZTdi',
            reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                                   txt_input_field=MESSAGES['main_input_field'])
        )

    elif message.text == MESSAGES['settings_btn_list'][4]:  # <<< Back
        await back_handl(message)
