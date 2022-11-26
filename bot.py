import logging
import sqlite3

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, markdown
import asyncio

from parser import add_news
from users_database import all_users_id, all_users_info, add_user
from news_database import get_unread_news
from config import TOKEN, admin

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def on_startup(_):
    await bot.send_message(admin, '<< Bot started >>')
    asyncio.create_task(always_update(900))


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    try:
        add_user(id, name, username)
        await bot.send_message(admin, f"New user\nID: {id}\nName: {name}\n@{username}", disable_notification=True)
        await bot.send_message(id, f"Привет {name}!\nВы успешно подписались на новости\nЖдите ближайшего обновления :)\n(каждые 15 минут)")
    except sqlite3.IntegrityError:
        await bot.send_message(id, 'Вы уже подписаны')
    except sqlite3.OperationalError:
        await bot.send_message(id, 'Не тыкай так часто :)')


@dp.message_handler(commands=['id'])
async def get_chat_id(message: types.Message):
    await bot.send_message(message.chat.id, message.chat.id)


@dp.message_handler(commands=['new'])
async def cmd_new(message: types.Message):
    if message.chat.type != 'private':
        await new_article()


@dp.message_handler(commands=['users_list'])
async def users_list(m: types.Message):
    if m.chat.type != 'private':
        users = all_users_info()
        for user in users:
            user_info = f'id: {str(user[0])}\n{user[1]}' + f'@{user[2]}' if user[2] != 'None' else ''
            await bot.send_message(admin, user_info)


@dp.message_handler(commands=['users_stat'])
async def users_stat(m: types.Message):
    if m.chat.type != 'private':
        users = all_users_info()
        await bot.send_message(admin, f'Users: {len(users)}')


async def always_update(update_time):
    await asyncio.sleep(5)
    await bot.send_message(admin, ' > Auto-update turned on ')
    while True:
        await new_article()
        await asyncio.sleep(update_time)


async def new_article():
    add_news()
    unread_news_list = get_unread_news()
    if unread_news_list != []:
        news_count = 0
        count = 0
        for news in unread_news_list:
            time_news = news[0]
            bold = markdown.bold(news[1])
            slim = news[2]
            link = news[3]
            hidden_link = markdown.link('Источник', link)
            msg = f'{time_news} {bold}{slim}\n{hidden_link}'
            msg = msg.replace('\\', '')
            users_id_list = all_users_id()
            for id in users_id_list:
                if count % 20 == 0 and count != 0:
                    await asyncio.sleep(2)
                else:
                    pass
                try:
                    await bot.send_message(id, msg, parse_mode='markdown', disable_web_page_preview=True)
                    count += 1
                except:
                    await bot.send_message(admin, f" ! Can't send to {id}")
            news_count += 1
        if news_count > 0:
            users_get_msg = count/news_count
        else:
            users_get_msg = 0
        await bot.send_message(admin, f' > Sent {news_count} news\n{count} messages at all\nAbout {users_get_msg} users')
    else:
        await bot.send_message(admin, ' > Ничего нового')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
