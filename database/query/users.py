from SETTINGS import db
from database.tables import TelegramUser


def get_user_by_tg_id(chat_id_user: int) -> TelegramUser:
    user = TelegramUser.get(chat_id_user=chat_id_user)
    return user


def db_get_access_id_users() -> list[int]:
    with db:
        users = TelegramUser.select().where(TelegramUser.status_user == 'regular_user')  # add date end paid > now
        return [user.chat_id_user for user in users]
