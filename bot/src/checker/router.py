from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.create_bot import bot

active_users = {
    1324716819,
    1853746545
}


checker_router = Router(name="checker_router")


@checker_router.message(Command("start"))
async def start(message: Message):
    active_users.add(message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        "Вы подписались на рассылку результатов ЕГЭ по информатике",
    )
