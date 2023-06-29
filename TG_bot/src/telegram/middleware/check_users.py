from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

from database.query.users import db_get_access_id_users


class CheckUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        allowed_users = db_get_access_id_users()
        if event.from_user.id in allowed_users:
            return await handler(event, data)
