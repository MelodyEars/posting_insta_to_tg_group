from typing import TypedDict

from .mine_USER_text import *


class Messages(TypedDict):
    start: str
    start_message: str
    help: str
    main_btn_list: list
    main_input_field: str
    settings_btn_list: list
    settings_input_field: str
    back: str


MESSAGES: Messages = {
    'start': start_message,
    'start_message': start_message,
    'help': help_message,

    'main_btn_list': main_btn_list,
    'main_input_field': main_input_field,

    'settings_btn_list': settings_btn_list,
    'settings_input_field': settings_input_field,

    'back': back
}


# ______________________________________________ Questions Setup insta ________________________________________________
class SetUpInstaMessages(TypedDict):
    quest_insta_login: str
    quest_insta_password: str
    success: str


SetUpInstaMessages: SetUpInstaMessages = {
    'quest_insta_login': quest_insta_login,
    'quest_insta_password': quest_insta_password,

    'success': success
}


# ______________________________________________ Questions Setup tiktok ________________________________________________
class SetUpTikTokMessages(TypedDict):
    quest_tiktok_login: str
    success: str


SetUpTikTokMessages: SetUpTikTokMessages = {
    'quest_tiktok_login': quest_tiktok_login,
    'success': success
}


# ______________________________________________ Questions Setup telegram _____________________________________________
class SetUpTelegramMessages(TypedDict):
    nickname_chanel: str
    success: str


SetUpTelegramMessages: SetUpTelegramMessages = {
    'nickname_chanel': nickname_chanel,
    'success': success
}


# ______________________________________________ Handling Error _____________________________________________
class ErrorMessages(TypedDict):
    request_attend_settings: str


ErrorMessages: ErrorMessages = {
    'request_attend_settings': request_attend_settings
}


# ______________________________________________ Successfully Actions _____________________________________________
class ProcessActions(TypedDict):
    begin_download: str
    download_success: str
    sent_success: str
    same_video: str


ProcessActions: ProcessActions = {
    'begin_download': begin_download,
    'download_success': download_success,
    'sent_success': sent_success,
    'same_video': same_video,
}