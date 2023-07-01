from SETTINGS import db
from database.tables import TelegramUser


def get_user_by_tg_id(chat_id_user: int) -> TelegramUser:
    user = TelegramUser.get(chat_id_user=chat_id_user)
    return user


def db_get_access_id_users(tg_chat_id: int) -> TelegramUser:
    with db:
        users = TelegramUser.get(chat_id_user=tg_chat_id)  # check date end paid > now and status user
        return users
