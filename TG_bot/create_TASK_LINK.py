

from loguru import logger
from typing import NamedTuple
from aiogram import types
from aiogram.fsm.state import State, StatesGroup

from NW_Upvoter.main_UPVOTER import start_reddit_work
from work_fs import auto_create, path_near_exefile


class RunBotStates(StatesGroup):
    reddit_link = State()
    upvote_int = State()


class StructData(NamedTuple):
    reddit_link: str
    upvote_int: int


async def run_process_and_reply_after(message: types.Message, data: StructData):
    logger.info("runner process")

    reddit_link = data.reddit_link
    upvote_int = data.upvote_int

    logger.add(
        auto_create(path_near_exefile("logs"), _type="dir") / "BaseReddit.log",
        format="{time} {level} {message}",
        level="INFO",
        rotation="10 MB",
        compression="zip"
    )

    await start_reddit_work(reddit_link, upvote_int, message)
