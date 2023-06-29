import asyncio
from concurrent.futures import ProcessPoolExecutor

from TG_bot.src.telegram.messages.user_msg import ProcessActions
from database.query.tt_work import db_add_downloaded_video
from database.tables import TikTokUser
from link_for_Download import TiktokDownloader


def get_video_from_tiktok(obj_tiktok_user: TikTokUser, all_video=False):
    video_records = []

    with TiktokDownloader(tt_name=obj_tiktok_user.username) as api:
        if not all_video:
            number_videos = api.get_all_video_by_tiktokname()[0]  # get latest video
        else:
            number_videos = api.get_all_video_by_tiktokname(scroll=True)

        for video_num in number_videos:
            name_video, video_path = api.get_info_video(video_num)
            video_record = {
                'tiktok_user': obj_tiktok_user,
                'number_video': video_num,
                'name_video': name_video,
                'path_video': video_path
            }
            video_records.append(video_record)

        api.DRIVER.quit()

    db_add_downloaded_video(video_records)


async def run_process_tt(obj_tiktok_user: TikTokUser, all_video=False):
    with ProcessPoolExecutor as executor:
        await asyncio.get_running_loop().run_in_executor(executor, get_video_from_tiktok, obj_tiktok_user, all_video)
