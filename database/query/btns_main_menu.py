from peewee import DoesNotExist

from SETTINGS import db
from database.tables import TikTokVideo, TikTokUser, TelegramUser


# _________________________________________________________________________________ TikTok
def db_get_tt_name_by_tg_id(tg_chat_id: int) -> TikTokUser or None:
    with db:
        try:
            user = TelegramUser.get(chat_id_user=tg_chat_id)
            # tiktok_user: TikTokUser = TikTokUser.get_or_none(TikTokUser.tg_id_user == user)
            tiktok_user = user.users.first()
            return tiktok_user
        except DoesNotExist:
            return None


def db_add_downloaded_video(video_record: dict):
    with db:
        TikTokVideo.create(**video_record)


def db_get_not_uploaded_videos() -> list[TikTokVideo]:
    with db:
        videos = TikTokVideo.select().where(TikTokVideo.is_uploaded == False)
        return videos


def db_update_uploaded_video(video: TikTokVideo):
    with db:
        video.is_uploaded = True
        video.save()


def db_get_all_videos_numbers(tt_user_obj: TikTokUser) -> list[int]:
    with db:
        videos_objs = TikTokVideo.select().where(TikTokVideo.tiktok_user == tt_user_obj)
        list_video_number = [obj_video.number_video for obj_video in videos_objs]
        return list_video_number


def db_upd_status_autoposting_tt(tt_user_obj: TikTokUser, status: bool):
    with db:
        tt_user_obj.autoposting_tt = status
        tt_user_obj.save()


def db_get_status_autopsting(tt_user_obj: TikTokUser) -> bool:
    with db:
        obj_tt_user = TikTokVideo.get_by_id(tt_user_obj.id)
        return obj_tt_user.autoposting_tt

