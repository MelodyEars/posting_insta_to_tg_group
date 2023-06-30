from peewee import DoesNotExist

from SETTINGS import db
from database.tables import TikTokVideo, TikTokUser, User


# _________________________________________________________________________________ TikTok
def db_get_tt_name_by_tg_id(telegram_id: int) -> TikTokUser or None:
    with db:
        try:
            user = User.get(User.id_telegram == telegram_id)
            # tiktok_user: TikTokUser = TikTokUser.get_or_none(TikTokUser.tg_id_user == user)
            tiktok_user = user.users.first()
            return tiktok_user
        except DoesNotExist:
            return None


def db_add_downloaded_video(video_records: list[dict]):
    with db:
        TikTokVideo.insert_many(video_records).execute()


def db_get_not_uploaded_videos() -> list[TikTokVideo]:
    with db:
        videos = TikTokVideo.select().where(TikTokVideo.is_uploaded == False)
        return videos


def db_update_uploaded_video(video: TikTokVideo):
    with db:
        video.is_uploaded = True
        video.save()
