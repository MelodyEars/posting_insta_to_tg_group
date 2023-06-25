

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def one_btn(text: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text)]
        ], resize_keyboard=True
    )


def many_btns(btns_text_list: list, txt_input_field: str, column_count=1) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for txt_btn in btns_text_list:
        builder.add(KeyboardButton(text=str(txt_btn)))
    builder.adjust(column_count)

    return builder.as_markup(resize_keyboard=True, input_field_placeholder=txt_input_field)


