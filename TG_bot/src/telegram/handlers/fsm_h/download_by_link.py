import asyncio
import re
from typing import NamedTuple

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from loguru import logger

from TG_bot.src.telegram.handlers.user_handlers.main_user_handlers import user_router
from TG_bot.src.telegram.buttons.user_btn import many_btns
from TG_bot.src.telegram.messages.user_msg import MESSAGES
from Tiktok.tt_output_dwnld_by_link import run_thread_tt_dwnld_video


class TikTokOneVideo(StatesGroup):
    link = State()


class StructData(NamedTuple):
    link: str


@user_router.message(F.text == MESSAGES['back'])
async def cancel_handler_download_one_video(message: Message, state: FSMContext, text=''):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    if text:
        await message.answer(
            text,
            reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                                   txt_input_field=MESSAGES['main_input_field'])
        )

    else:
        await message.answer(
            '@MessHub_bot',
            reply_markup=many_btns(btns_text_list=MESSAGES['main_btn_list'],
                                   txt_input_field=MESSAGES['main_input_field'])
        )


@user_router.message(TikTokOneVideo.link)
async def answer_wish_tt_video_link(message: Message, state: FSMContext):
    link = message.text
    logger.info("link for download tiktok video: " + link)

    # Регулярний вираз для отримання номера відео та перевірки шаблону
    pattern_comp = r"https:\/\/www\.tiktok\.com\/@.+?\/video\/(\d+)\/?$"

    # 'https://vm.tiktok.com/ZM29gPj5W/'
    pattern_mobile = r"https:\/\/(?:www\.)?vm\.tiktok\.com\/([a-zA-Z0-9]+)\/?$"

    # Застосовуємо регулярний вираз до посилання
    match_comp_link = re.search(pattern_comp, link)
    math_mobile_link = re.search(pattern_mobile, link)

    if match_comp_link or math_mobile_link:
        await state.update_data(link=link)
        data = await state.get_data()
        struct_data = StructData(**data)

        link = struct_data.link
        task = asyncio.create_task(run_thread_tt_dwnld_video(group_chat_id=message.chat.id, link=link))

        # send msg
        await cancel_handler_download_one_video(message, state, text="Your video is downloading...")

        await task
        # TODO add ads from adnmin link
        # await message.answer()
    else:
        # if not match
        await cancel_handler_download_one_video(message, state, text=f'''
        Please, send correct link as
        https://www.tiktok.com/@kherson2day/video/7252772763570539782?_t=8doziYwEvRd
        or
        https://vm.tiktok.com/ZM29gPj5W/''')


