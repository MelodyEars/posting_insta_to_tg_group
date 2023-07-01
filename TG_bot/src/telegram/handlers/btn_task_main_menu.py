import time

from aiogram.types import Message, FSInputFile

from TG_bot.setup import bot
from TG_bot.src.telegram.messages.user_msg import ProcessActions
from Tiktok import run_thread_tt
from database.query.btns_main_menu import db_get_not_uploaded_videos, db_update_uploaded_video, \
    db_upd_status_autoposting_tt, db_get_status_autopsting, db_get_tt_name_by_tg_id
from database.tables import TikTokUser, TikTokVideo


async def send_msg_from_db_to_chat(group_chat_id: int):
    obj_for_send: list[TikTokVideo] = db_get_not_uploaded_videos()

    for obj_video in obj_for_send:
        video_from_pc = FSInputFile(obj_video.path_video)

        await bot.send_video(
            chat_id=group_chat_id, video=video_from_pc,
            caption=obj_video.name_video + "\n@MessHub_bot"
        )

        db_update_uploaded_video(obj_video)


async def tiktok_btn_task(message: Message, obj_tiktok_user: TikTokUser, group_chat_id: int):
    await message.answer(ProcessActions['begin_download'], )

    # run browser and add downloaded video to db
    msg = await run_thread_tt(obj_tiktok_user)
    await message.answer(msg)

    if msg != ProcessActions['sent_success']:
        return

    await message.answer(ProcessActions['download_success'])
    # send video to telegram chat
    await send_msg_from_db_to_chat(group_chat_id)
    await message.answer(ProcessActions['sent_success'])


async def autoposting_tt_inline_btn_task(message: Message, obj_tiktok_user: TikTokUser, group_chat_id: int):
    autoposting = True

    db_upd_status_autoposting_tt(obj_tiktok_user, autoposting)

    while autoposting:
        # run browser and add downloaded video to db
        msg = await run_thread_tt(obj_tiktok_user)

        if msg == ProcessActions['sent_success']:
            # send video to telegram chat
            await send_msg_from_db_to_chat(group_chat_id)
            await message.answer(ProcessActions['sent_success'])

        time.sleep(60 * 5)  # 5 min
        autoposting = db_get_status_autopsting(obj_tiktok_user)


async def stop_autoposting_tt_inline_btn_task(message: Message):
    autoposting = False

    obj_tiktok_user = db_get_tt_name_by_tg_id(message.from_user.id)
    db_upd_status_autoposting_tt(obj_tiktok_user, autoposting)


