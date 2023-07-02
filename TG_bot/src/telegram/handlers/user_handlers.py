
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from loguru import logger

from TG_bot.setup import user_router
from TG_bot.src.telegram.buttons.user_btn import one_btn, many_btns, one_inline_btn
from TG_bot.src.telegram.handlers.fsm_h.setup_instagram import SetUpInstagram
from TG_bot.src.telegram.handlers.fsm_h.setup_telegram import SetUpTelegram
from TG_bot.src.telegram.handlers.fsm_h.setup_tiktok import SetUpTikTok
from TG_bot.src.telegram.messages.user_msg import (MESSAGES, SetUpInstaMessages, SetUpTikTokMessages,
                                                   SetUpTelegramMessages, ErrorMessages)
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
    await message.reply(
        "ㅤ",
        reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                               txt_input_field=MESSAGES['main_input_field'])
    )


@user_router.message(F.text.in_(MESSAGES['main_btn_list']))
async def starter_work(message: Message):
    logger.info("starter_work")
    if message.text == MESSAGES['main_btn_list'][0]:  # TikTok
        # TODO tiktokapi not have video on tiktok page
        logger.info("TikTok")
        obj_tiktok_user: TikTokUser = db_get_tt_name_by_tg_id(message.chat.id)
        group_chat_id = get_user_by_tg_id(message.chat.id).group_chat_id

        if not (obj_tiktok_user is None and group_chat_id is None):
            if not obj_tiktok_user.autoposting_tt:
                # still not run autoposting
                logger.info("still not run autoposting")
                builder = one_inline_btn("Run autoposting", "start_tt_auto")
                await message.answer("Starting TikTok", reply_markup=builder.as_markup())

            else:
                # already run autoposting
                logger.info("already run autoposting")
                builder = one_inline_btn("Turn OFF autoposting", "end_tt_auto")
                await message.answer("Tiktok was started", reply_markup=builder.as_markup())

        else:
            await message.answer(ErrorMessages['request_attend_settings'] + 'Tiktok')
            # Todo add inline-button for setup tiktok and telegram

    elif message.text == MESSAGES['main_btn_list'][1]:  # Settings
        await message.answer(
            'ㅤ',
            reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                                   txt_input_field=MESSAGES['settings_input_field'])
        )


@user_router.message(F.text.in_(MESSAGES['settings_btn_list']))
async def setup_social_network(message: Message,  state: FSMContext):
    # if message.text == MESSAGES['settings_btn_list'][0]:  # SetUP TikTok
    #     await state.set_state(SetUpTikTok.tiktok_login)
    #     await message.reply(SetUpTikTokMessages['quest_tiktok_login'], reply_markup=one_btn(MESSAGES['back']))

    if message.text == MESSAGES['settings_btn_list'][0]:  # SetUP Instagram
        await state.set_state(SetUpInstagram.insta_login)
        await message.reply(SetUpInstaMessages['quest_insta_login'], reply_markup=one_btn(MESSAGES['back']))

    elif message.text == MESSAGES['settings_btn_list'][1]:  # SetUP Telegram
        await state.set_state(SetUpTelegram.link_your_chanel)
        await message.reply(SetUpTelegramMessages['nickname_chanel'], reply_markup=one_btn(MESSAGES['back']))

    elif message.text == MESSAGES['settings_btn_list'][2]:  # <<< Back
        await message.answer(
            'ㅤ',
            reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                                   txt_input_field=MESSAGES['main_input_field'])
        )
