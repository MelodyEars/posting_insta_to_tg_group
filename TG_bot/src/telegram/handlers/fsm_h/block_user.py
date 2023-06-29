from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from TG_bot.setup import admin_router
from database.tables import User
from TG_bot.src.telegram.messages.admin_msg import admin_MESSAGES

blocked_users = []


class DeleteUser(StatesGroup):
    username = State()


class AddUser(StatesGroup):
    username = State()


@admin_router.message(DeleteUser.username)
async def block(message: Message, state: FSMContext):
    user = User.get_or_none(id_telegram=message.text)
    if user:
        user.delete_instance()
        await message.reply(f"{message.text} " + admin_MESSAGES['deleted_user'],
                            parse_mode='MARKDOWN')
    else:
        await message.reply(admin_MESSAGES['user_denied'])

    await state.clear()


@admin_router.message(AddUser.username)
async def unblock(message: Message, state: FSMContext):
    try:
        int_id_tg = int(message.text)
        user, created = User.get_or_create(id_telegram=int_id_tg)
    except ValueError:
        await message.reply(admin_MESSAGES['error_enter_username'])
        return

    if created:
        await message.reply(f"{message.text}" + admin_MESSAGES['added_user'],
                            parse_mode='MARKDOWN')
    else:
        await message.reply(admin_MESSAGES['has_access'])
    await state.clear()

