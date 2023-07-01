from SETTINGS import db
from database.tables import TelegramUser, TikTokUser


# _______________________________________________________________________________ TIKTOK
def db_create_TT_user(tt_username: str, id_chat_user: int):
    with db:
        user: TelegramUser = TelegramUser.get_or_none(chat_id_user=id_chat_user)
        obj_tt_user, created, = TikTokUser.get_or_create(tg_id_user=user, username=tt_username)

        obj_tt_user.username = tt_username
        obj_tt_user.save()


# _______________________________________________________________________________ TELEGRAM
def db_add_tg_groupname(group_chat_id, id_chat_user: int, group_name_chat: str):
    user: TelegramUser = TelegramUser.get_or_none(chat_id_user=id_chat_user)
    if user is not None:
        user.group_chat_id = group_chat_id
        user.group_name_chat = group_name_chat
        user.save()
