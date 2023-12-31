import time
from pathlib import Path

from aiogram.types import Message, FSInputFile
from loguru import logger

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
            caption=obj_video.name_video + "\n\n Powered by @MessHub_bot"
        )

        db_update_uploaded_video(obj_video)
        Path(obj_video.path_video).unlink()  # del video from folder /tiktok_video


async def autoposting_tt_inline_btn_task(obj_tiktok_user: TikTokUser, group_chat_id: int):
    """
    Run autoposting task for every tiktok user.
     Open browser every 5 minutes and check new one video,
      download video if number of video not in db , send to telegram chat
       """

    autoposting = True

    logger.info("start autoposting tt inline btn task")
    db_upd_status_autoposting_tt(obj_tiktok_user, autoposting)

    while autoposting:
        logger.info(f"autoposting run for {obj_tiktok_user.username}")
        # run browser and add downloaded video to db
        msg = await run_thread_tt(obj_tiktok_user)

        if msg == ProcessActions['sent_success']:
            logger.info("new video was sent to chat")
            # send video to telegram chat
            await send_msg_from_db_to_chat(group_chat_id)
            await bot.send_message(chat_id=group_chat_id, text=ProcessActions['sent_success'])

        logger.info(f"autoposting sleep for {obj_tiktok_user.username}")
        time.sleep(60 * 5)  # 5 min

        autoposting = db_get_status_autopsting(obj_tiktok_user)
        logger.info(f"autoposting status {autoposting} for {obj_tiktok_user.username}")


async def stop_autoposting_tt_inline_btn_task(group_chat_id):
    """ Change status autoposting to False in db """
    autoposting = False
    logger.info("stop autoposting tt inline btn task")

    obj_tiktok_user = db_get_tt_name_by_tg_id(group_chat_id)
    db_upd_status_autoposting_tt(obj_tiktok_user, autoposting)

