from loguru import logger
from peewee import DoesNotExist

from SETTINGS import db
from database.tables import TikTokVideo, TikTokUser, TelegramUser


# _________________________________________________________________________________ TikTok
def db_get_tt_name_by_tg_id(tg_chat_id: int) -> TikTokUser or None:
    with db:
        user = TelegramUser.get(chat_id_user=tg_chat_id)
        logger.info(f"get tt name by tg id: {user.tg_username}")
        # tiktok_user: TikTokUser = TikTokUser.get_or_none(TikTokUser.tg_id_user == user)
        tiktok_user = user.telegram_users.first()
        return tiktok_user

def db_add_downloaded_video(video_record: dict):
    logger.info(f"add downloaded video to db: {video_record}")

    with db:
        TikTokVideo.create(**video_record)


def db_get_not_uploaded_videos() -> list[TikTokVideo]:
    logger.info("get not uploaded videos")

    with db:
        videos = TikTokVideo.select().where(TikTokVideo.is_uploaded == False)
        return videos


def db_update_uploaded_video(video: TikTokVideo):
    logger.info(f"update uploaded video: {video.name_video}")

    with db:
        video.is_uploaded = True
        video.save()


def db_get_all_videos_numbers(tt_user_obj: TikTokUser) -> list[int]:
    logger.info(f"get all videos numbers for tt user: {tt_user_obj.username}")

    with db:
        videos_objs = TikTokVideo.select().where(TikTokVideo.tiktok_user == tt_user_obj)
        list_video_number = [obj_video.number_video for obj_video in videos_objs]
        return list_video_number


def db_upd_status_autoposting_tt(tt_user_obj: TikTokUser, status: bool):
    logger.info(f"update status autoposting tt: {status}")

    with db:
        tt_user_obj.autoposting_tt = status
        tt_user_obj.save()


def db_get_status_autopsting(tt_user_obj: TikTokUser) -> bool:
    logger.info(f"get status autoposting tt: {tt_user_obj.autoposting_tt}")

    with db:
        obj_tt_user = TikTokUser.get_by_id(tt_user_obj.id)
        return obj_tt_user.autoposting_tt

