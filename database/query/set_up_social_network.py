from SETTINGS import db
from database.tables import User, TikTokUser


# _______________________________________________________________________________ TIKTOK
def db_create_TT_user(username: str, id_telegram: int):
    with db.atomic():
        user = User.get_or_none(id_telegram=id_telegram)
        if user is None:
            tiktok_user = TikTokUser.create(tg_id_user=user, username=username)
            return tiktok_user


# _______________________________________________________________________________ TELEGRAM
def db_add_tg_groupname(group_chat_id: int, id_telegram: int):
    user = User.get_or_none(id_telegram=id_telegram)
    if user is not None:
        user.group_chat_id = group_chat_id
        user.save()
