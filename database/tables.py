import peewee as pw

from datetime import datetime

from SETTINGS import db


class BaseModel(pw.Model):
    id = pw.PrimaryKeyField(unique=True)

    class Meta:
        database = db


class User(BaseModel):
    id_telegram = pw.IntegerField(unique=True)
    status_user = pw.CharField(default='regular_user')
    name_group_telegram = pw.CharField(default=None, null=True)
    date_registration = pw.DateTimeField(default=datetime.now)
    date_paid = pw.DateTimeField(default=None, null=True)
    date_end_paid = pw.DateTimeField(default=None, null=True)

    class Meta:
        db_table = 'users'


class TikTokUser(BaseModel):
    tg_id_user = pw.ForeignKeyField(User, backref="users", on_delete='CASCADE')
    username = pw.CharField(max_length=100)
    access_tg_user = pw.BooleanField(default=True)

    class Meta:
        db_table = 'tiktok_users'


class TikTokVideo(BaseModel):

    tiktok_user = pw.ForeignKeyField(TikTokUser, backref="tiktok_users", on_delete='СASCADE')
    number_video = pw.IntegerField(unique=True)
    name_video = pw.CharField()
    path_video = pw.CharField()
    date_download = pw.DateTimeField(default=datetime.now)
    is_uploaded = pw.BooleanField(default=False)

    class Meta:
        db_table = 'tiktok_videos'


def create_tables_user_tg():
    db.create_tables([User, TikTokUser, TikTokVideo])
