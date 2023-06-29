from SETTINGS import db
from database.tables import TikTokVideo, TikTokUser, User


def db_get_tt_name_by_tg_id(telegram_id) -> TikTokUser or None:
    with db:
        try:
            tiktok_user: TikTokUser = TikTokUser.select().join(User).where(User.id_telegram == telegram_id).get()
            return tiktok_user
        except User.DoesNotExist:
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