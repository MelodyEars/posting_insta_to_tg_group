from SETTINGS import db
from database.tables import User


def db_add_user(chat_id_user: int, tg_username: str):
    with db:
        User.get_or_create(chat_id_user=chat_id_user, tg_username=tg_username)
