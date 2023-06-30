import asyncio
from concurrent.futures import ProcessPoolExecutor

from TG_bot.src.telegram.messages.user_msg import ProcessActions
from database.query.btns_main_menu import db_add_downloaded_video, db_get_all_videos_numbers
from database.tables import TikTokUser
from .link_for_Download import TiktokDownloader


def get_video_from_tiktok(obj_tiktok_user: TikTokUser, all_video=False):
    message = ProcessActions['sent_success']
    list_number_videos = db_get_all_videos_numbers(obj_tiktok_user)
    print(f"list number video {list_number_videos}")
    tt_name = obj_tiktok_user.username

    with TiktokDownloader(tt_name=tt_name) as api:
        if not all_video:
            list_videos = [api.get_all_video_by_tiktokname()[0]]
        else:
            list_videos = api.get_all_video_by_tiktokname(scroll=True)

        for video_num in list_videos:
            print(f"{video_num} in {list_number_videos}")
            print(f"type {type(video_num)}, type in list {type(list_number_videos[0])}")
            if video_num not in list_number_videos:
                name_video, video_path = api.get_info_video(video_num)
                video_record = {
                    'tiktok_user': obj_tiktok_user,
                    'number_video': video_num,
                    'name_video': name_video,
                    'path_video': video_path
                }

                db_add_downloaded_video(video_record)
            else:
                message = ProcessActions['same_video']

        api.DRIVER.quit()

    return message


async def run_process_tt(obj_tiktok_user: TikTokUser, all_video=False):
    with ProcessPoolExecutor() as executor:
        msg = await asyncio.get_running_loop().run_in_executor(executor, get_video_from_tiktok, obj_tiktok_user,
                                                               all_video)

    return msg

