from SETTINGS import db
from database.tables import TikTokVideo


def db_add_downloaded_video(video_records: list[dict]):
    with db:
        TikTokVideo.insert_many(video_records).execute()
