from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove

import json

from config import TOKEN, RECEIVER, GROUP_ID
from extensions import (
        send_hello, 
        help_reply_keyboard, 
        send_help, 
        send_top_list, 
        send_start_con, 
        add_user, 
        delete_user
)

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(lambda message: message.chat.id == RECEIVER, commands=['start'])
async def start(message: types.Message) -> None:
    await message.answer(text = send_hello(message.from_user.full_name),
    reply_markup=help_reply_keyboard)


@dp.message_handler(lambda message: message.chat.id == RECEIVER, commands=['help'])
async def help(message: types.Message) -> None:
    await message.answer(text = send_help(),
    reply_markup=ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.chat.id == RECEIVER, commands=['top'])
async def top(message: types.Message) -> None:
    await bot.send_message(chat_id=RECEIVER,text = send_top_list(), parse_mode='html')


@dp.message_handler(lambda message: message.chat.id == RECEIVER, commands=['start_count'])
async def start_con(message: types.Message) -> None:
    with open('users_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    try:
        del data
        data = {}
    except:
        pass

    with open('users_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, fp=f)
    await message.reply(text=send_start_con())

@dp.message_handler(lambda message: message.chat.id == GROUP_ID, content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def added_user(message: types.Message):

    res = add_user(message)

    if res == 'added_bot':
        await message.reply(text=f"{message.from_user.full_name} iltimos bot qo'shmang!")
    elif res == 'bot_added':
        await message.rerly(text=f"{message.from_user.full_name} Bot guruhga odam qo'sha olmaydi!")
    else:
        pass
    await bot.delete_message(chat_id = message.chat.id, message_id = message["message_id"])

@dp.message_handler(lambda message: message.chat.id == GROUP_ID, content_types= types.ContentTypes.LEFT_CHAT_MEMBER)
async def deleting_user(message: types.Message):
    user_id = message["left_chat_member"]["id"]
    delete_user( user_id=user_id )
    await bot.delete_message(chat_id = message.chat.id, message_id = message["message_id"])


if __name__ == "__main__":
    executor.start_polling(dp,
        skip_updates=True)