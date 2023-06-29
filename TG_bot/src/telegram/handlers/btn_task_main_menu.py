
from aiogram.types import Message, FSInputFile

from TG_bot.setup import bot
from TG_bot.src.telegram.messages.user_msg import ProcessActions
from Tiktok import run_process_tt
from database.query.tt_work import db_get_not_uploaded_videos
from database.tables import TikTokUser, TikTokVideo


async def send_msg_from_db_to_chat(group_chat_id: int):
    # TODO get message from db and send to chat
    obj_for_send: list[TikTokVideo] = db_get_not_uploaded_videos()

    for obj_video in obj_for_send:
        video_from_pc = FSInputFile(obj_video.path_video)
        await bot.send_photo(chat_id=group_chat_id, photo=video_from_pc, caption=obj_video.name_video)
        db_get_not_uploaded_videos(obj_video)


async def tiktok_btn_task(message: Message, obj_tiktok_user: TikTokUser, group_chat_id: int):
    await message.answer(ProcessActions['begin_download'], )

    # run browser and add downloaded video to db
    await run_process_tt(obj_tiktok_user)
    await message.answer(ProcessActions['download_success'])
    # send video to telegram chat
    await send_msg_from_db_to_chat(group_chat_id)
    await message.answer(ProcessActions['sent_success'])
