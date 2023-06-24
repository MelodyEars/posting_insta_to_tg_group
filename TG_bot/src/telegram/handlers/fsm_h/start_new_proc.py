import asyncio

from loguru import logger

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from TG_bot.setup import user_router
from TG_bot.src.telegram.buttons.user_btn import main_btn
from TG_bot.src.telegram.messages.user_msg import MESSAGES
from TG_bot.create_TASK_LINK import run_process_and_reply_after, RunBotStates, StructData
from SETTINGS import COUNT_BOT


@user_router.message(F.text == MESSAGES['btn_reset'])
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.reply(MESSAGES['reset_msg'], reply_markup=main_btn)


@user_router.message(RunBotStates.reddit_link)
async def answer_link(message: Message, state: FSMContext):
    await state.set_state(RunBotStates.upvote_int)
    await state.update_data(reddit_link=message.text)

    await message.reply(MESSAGES['upvote_int'])


@user_router.message(RunBotStates.upvote_int)
async def answer_vote(message: Message, state: FSMContext):
    try:
        upvote_int = int(message.text)

        if upvote_int <= COUNT_BOT:
            await state.update_data(upvote_int=upvote_int)
        else:
            await state.clear()
            await message.reply(MESSAGES['error_vote_int_2'], reply_markup=main_btn)
            return

    except ValueError:
        await state.clear()
        await message.reply(MESSAGES['error_vote_int'],
                            reply_markup=main_btn)
        return

    data = await state.get_data()
    struct_data = StructData(**data)

    logger.info(struct_data.reddit_link)
    logger.info(struct_data.upvote_int)

    try:
        run_process = asyncio.create_task(run_process_and_reply_after(message, struct_data))

        await state.clear()
        await message.answer(str(MESSAGES['notif_browser_run'] + data["reddit_link"]), reply_markup=main_btn)

        await run_process
    except Exception:
        await message.answer(MESSAGES['process_wrong'], reply_markup=main_btn)
