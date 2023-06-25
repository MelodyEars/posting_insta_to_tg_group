from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from TG_bot.setup import admin_router
from TG_bot.src.database.tables import AllowedUser
from TG_bot.src.telegram.messages.admin_msg import admin_MESSAGES

blocked_users = []


class DeleteUser(StatesGroup):
    username = State()


class AddUser(StatesGroup):
    username = State()


@admin_router.message(DeleteUser.username)
async def block(message: Message, state: FSMContext):
    user = AllowedUser.get_or_none(username=message.text)
    if user:
        user.delete_instance()
        await message.reply(f"{message.text} " + admin_MESSAGES['deleted_user'],
                            parse_mode='MARKDOWN')
    else:
        await message.reply(admin_MESSAGES['user_denied'])

    await state.clear()


@admin_router.message(AddUser.username)
async def unblock(message: Message, state: FSMContext):
    user, created = AllowedUser.get_or_create(username=message.text)

    if created:
        await message.reply(f"{message.text}" + admin_MESSAGES['added_user'],
                            parse_mode='MARKDOWN')
    else:
        await message.reply(admin_MESSAGES['has_access'])
    await state.clear()

