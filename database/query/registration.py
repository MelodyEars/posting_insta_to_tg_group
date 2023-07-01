from SETTINGS import db
from database.tables import User


def db_add_user(int_id_tg):
    with db:
        User.get_or_create(id_telegram=int_id_tg)
