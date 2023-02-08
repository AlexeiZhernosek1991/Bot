from aiogram.contrib.fsm_storage.memory import MemoryStorage

from googl_sheet import *
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command
import config_bot
import keyboard
import logging

storage = MemoryStorage()
bot = Bot(config_bot.TOKEN)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(filename='log.txt', filemode='a',
                    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

sheet = Table('credentials.json', "Копия Промокоды").get_sheet_list()


@dp.message_handler(Command('start'), start=None)
async def welcome(message):
    await bot.send_message(message.chat.id, text='Выберите категорию в которой хотите получить скидку ⬇️',
                           reply_markup=keyboard.get_start(), parse_mode='Markdown')


@dp.callback_query_handler(text_contains="get_start")
async def start(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.message.chat.id, text='Выберите категорию в которой хотите получить скидку ⬇️',
                           reply_markup=keyboard.get_start(), parse_mode='Markdown')


@dp.callback_query_handler(text_contains="s")
async def all_category(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.message.chat.id, text=f'Выбирайте 🥰',
                           reply_markup=keyboard.get_button(keyboard.dict_[call.data[1:]]), parse_mode='Markdown')


@dp.callback_query_handler(text_contains="m")
async def marketplace(call: types.CallbackQuery):
    list_rows = get_list_row(sheet, call.data[1:])
    await bot.send_message(chat_id=call.message.chat.id,
                           text='Чтобы успешно активировать промокод👌 достаточно: '
                                'перейти по ссылке или скопировать '
                                'значение купона с данной страницы и ввести его на сайте компании☺️')
    for row in list_rows:
        await bot.send_message(chat_id=call.message.chat.id, text=f'Название: {row[0]}\n'
                                                                  f'Скидка: {row[3]}\n'
                                                                  f'Описание: {row[7]}\n'
                                                                  f'Действует до: {row[5]}\n'
                                                                  f'Регион: {row[6]}\n'
                                                                  f'Ссылка: {row[4]}\n'
                                                                  f'Промокод ниже👇')
        await bot.send_message(chat_id=call.message.chat.id, text=f'{row[2]}')
    buttons = [
        types.InlineKeyboardButton(text=f"{list_rows[0][8]}", callback_data=f's{list_rows[0][8]}'),
        types.InlineKeyboardButton(text="Главное меню", callback_data='get_start')
    ]
    keyboard_ = types.InlineKeyboardMarkup(row_width=1)
    keyboard_.add(*buttons)
    await bot.send_message(chat_id=call.message.chat.id, text='Куда отправимся за скидками',
                           reply_markup=keyboard_, parse_mode='Markdown')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
