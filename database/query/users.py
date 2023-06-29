from SETTINGS import db
from database.tables import User


def get_user_by_tg_id(telegram_id) -> User:
    user = User.get(User.id_telegram == telegram_id)
    return user


def db_get_access_id_users() -> list[int]:
    with db:
        users = User.select().where(User.status_user == 'regular_user')  # add date end paid > now
        return [user.id_telegram for user in users]

