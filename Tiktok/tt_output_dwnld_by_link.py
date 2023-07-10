import asyncio
from concurrent.futures import ThreadPoolExecutor

from aiogram.types import FSInputFile, InputFile
from loguru import logger

from TG_bot.setup import bot
from .link_for_Download import TiktokDownloader


def get_video_from_tiktok(link: str):
    with TiktokDownloader() as api:
        name_video, video_path = api.get_info_video(url_tiktok_video=link)
        api.DRIVER.quit()

    return name_video, video_path


async def run_thread_tt_dwnld_video(group_chat_id, link):
    # _______________________________________ Open browser and download video
    with ThreadPoolExecutor() as executor:
        name_video, video_path = await asyncio.get_running_loop().run_in_executor(executor, get_video_from_tiktok, link)

    # _______________________________________ TG send message
    logger.info(f"Send video as video {video_path}")
    video_from_pc = FSInputFile(video_path)

    await bot.send_video(
        chat_id=group_chat_id,
        video=video_from_pc,
        caption=name_video + "\n\n Best regards! @MessHub_bot"
    )

    logger.info(f"Delete video {video_path}")
    video_path.unlink()
