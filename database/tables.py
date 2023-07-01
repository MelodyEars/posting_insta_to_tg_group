import peewee as pw

from datetime import datetime

from SETTINGS import db


class BaseModel(pw.Model):
    id = pw.PrimaryKeyField(unique=True)

    class Meta:
        database = db


class TelegramUser(BaseModel):
    tg_username = pw.CharField(max_length=100, null=True)
    chat_id_user = pw.BigIntegerField(unique=True)

    group_name_chat = pw.BigIntegerField(default=None, null=True)
    group_chat_id = pw.BigIntegerField(default=None, null=True)

    status_user = pw.CharField(default='regular_user')

    date_registration = pw.DateTimeField(default=datetime.now)
    date_paid = pw.DateTimeField(default=None, null=True)
    date_end_paid = pw.DateTimeField(default=None, null=True)

    class Meta:
        db_table = 'telegram_users'


class TikTokUser(BaseModel):
    tg_id_user = pw.ForeignKeyField(TelegramUser, backref="telegram_users", on_delete='CASCADE')
    username = pw.CharField(max_length=100, null=True, default=None)
    access_tg_user = pw.BooleanField(default=True)
    autoposting_tt = pw.BooleanField(default=False)

    class Meta:
        db_table = 'tiktok_users'


class TikTokVideo(BaseModel):

    tiktok_user = pw.ForeignKeyField(TikTokUser, backref="tiktok_users", on_delete='CASCADE')
    number_video = pw.BigIntegerField(unique=True)
    name_video = pw.CharField()
    path_video = pw.CharField()
    date_download = pw.DateTimeField(default=datetime.now)
    is_uploaded = pw.BooleanField(default=False)

    class Meta:
        db_table = 'tiktok_videos'


def create_tables_user_tg():
    db.create_tables([TelegramUser, TikTokUser, TikTokVideo])
