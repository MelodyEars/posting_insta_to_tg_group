import asyncio

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from TG_bot.setup import user_router
from TG_bot.src.telegram.buttons.user_btn import one_btn, many_btns
from TG_bot.src.telegram.handlers.fsm_h.setup_instagram import SetUpInstagram
from TG_bot.src.telegram.handlers.fsm_h.setup_telegram import SetUpTelegram
from TG_bot.src.telegram.handlers.fsm_h.setup_tiktok import SetUpTikTok
from TG_bot.src.telegram.messages.user_msg import MESSAGES, SetUpInstaMessages, SetUpTikTokMessages, \
    SetUpTelegramMessages, ErrorMessages, ProcessActions
from database.query.users import db_get_tt_name_by_tg_id, get_user_by_tg_id

from Tiktok import run_process_tt


@user_router.message(Command(commands='start'))
async def start(message: Message):
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
    if message.text == MESSAGES['main_btn_list'][0]:  # Instagram
        await message.answer('Unfortunately, this feature is not available yet',)
        # TODO create task

    elif message.text == MESSAGES['main_btn_list'][1]:  # TikTok
        # TODO check status for download all videos
        if (
                (obj_tiktok_user := db_get_tt_name_by_tg_id(message.from_user.id)) and
                (name_group_telegram := get_user_by_tg_id(message.from_user.id).name_group_telegram is not None)
        ):
            await message.answer(ProcessActions['begin_download'],)
            # run browser and add downloaded video to db
            download_one = asyncio.create_task(run_process_tt(obj_tiktok_user))
            msg = await download_one
            await message.answer(msg)
            # TODO send video to telegram chanel
        else:
            await message.answer(ErrorMessages['request_attend_settings'] + 'Tiktok',)
            # Todo add inline-button for setup tiktok and telegram

    elif message.text == MESSAGES['main_btn_list'][2]:  # Settings
        await message.answer(
            'ㅤ',
            reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                                   txt_input_field=MESSAGES['settings_input_field'])
        )


# TODO Check all videos in db and send to telegram chanel

@user_router.message(F.text.in_(MESSAGES['settings_btn_list']))
async def setup_social_network(message: Message,  state: FSMContext):
    if message.text == MESSAGES['settings_btn_list'][0]:  # SetUP TikTok
        await state.set_state(SetUpTikTok.tiktok_login)
        await message.reply(SetUpTikTokMessages['quest_tiktok_login'], reply_markup=one_btn(MESSAGES['back']))

    elif message.text == MESSAGES['settings_btn_list'][1]:  # SetUP Instagram
        await state.set_state(SetUpInstagram.insta_login)
        await message.reply(SetUpInstaMessages['quest_insta_login'], reply_markup=one_btn(MESSAGES['back']))

    elif message.text == MESSAGES['settings_btn_list'][2]:  # SetUP Telegram
        await state.set_state(SetUpTelegram.api_id)
        await message.reply(SetUpTelegramMessages['quest_telegram_id'], reply_markup=one_btn(MESSAGES['back']))

    elif message.text == MESSAGES['settings_btn_list'][3]:  # <<< Back
        await message.answer(
            'ㅤ',
            reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                                   txt_input_field=MESSAGES['main_input_field'])
        )
