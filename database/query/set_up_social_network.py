from SETTINGS import db
from database.tables import User, TikTokUser


# _______________________________________________________________________________ TIKTOK
def db_create_TT_user(tt_username: str, id_telegram: int):
    with db:
        user = User.get(id_telegram=id_telegram)
        TikTokUser.create(tg_id_user=user, username=tt_username)


# _______________________________________________________________________________ TELEGRAM
def db_add_tg_groupname(group_chat_id, id_telegram: int):
    user = User.get_or_none(id_telegram=id_telegram)
    if user is not None:
        user.group_chat_id = group_chat_id
        user.save()
