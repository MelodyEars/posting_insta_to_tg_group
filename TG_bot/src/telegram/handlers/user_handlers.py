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
    SetUpTelegramMessages


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
        "",
        reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                               txt_input_field=MESSAGES['main_input_field'])
    )


@user_router.message(F.text.in_(MESSAGES['main_btn_list']))
async def starter_work(message: Message):
    if message.text == MESSAGES['main_btn_list'][0]:  # Instagram
        await message.answer('OK INSTAGRAM in work',)
        # TODO create task

    elif message.text == MESSAGES['main_btn_list'][1]:  # TikTok
        await message.answer('OK TIKTOK in work',)
        # TODO create task

    elif message.text == MESSAGES['main_btn_list'][2]:  # Settings
        await message.answer(
            '',
            reply_markup=many_btns(btns_text_list=MESSAGES['settings_btn_list'],
                                   txt_input_field=MESSAGES['settings_input_field'])
        )


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
            '',
            reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                                   txt_input_field=MESSAGES['main_input_field'])
        )
