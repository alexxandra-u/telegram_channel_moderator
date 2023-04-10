from aiogram import types
from create_bot import bot, dp
from parsers.vk_parser import VkParser
from parsers.youtube_parser import YoutubeParser
from handlers.database_communicator import DatabaseCommunicator
from handlers.channel_communicator import ChannelCommunicator
from utils.keyboards import KeyboardCreator
from utils.messages import UserMessages
import time
import datetime
import validators


class UserCommunicator:

    @dp.message_handler(commands=['start', 'help'])
    async def process_start_command(message: types.Message):
        await message.answer(UserMessages.start_mes)

    @dp.message_handler(commands=['set_channel'])
    async def set_channel(message: types.Message):
        channel = DatabaseCommunicator.sql_read_channel(message.from_user.id)
        has_moderated_channel = (len(channel) > 0)
        if not has_moderated_channel:
            await message.answer(UserMessages.set_channel_mes_2, reply_markup=KeyboardCreator.set_channel_keyboard())
        else:
            await message.answer(UserMessages.set_channel_mes_1 + channel[0][1],
                                 reply_markup=KeyboardCreator.reset_channel_keyboard())

    @dp.message_handler(commands=["add_new_source"])
    async def add_new_source(message: types.Message):
        has_moderated_channel = len(DatabaseCommunicator.sql_read_channel(message.from_user.id)) > 0
        if not has_moderated_channel:
            await message.answer(UserMessages.no_channel_mes)
        else:
            await message.answer(UserMessages.source_choice_mes, reply_markup=KeyboardCreator.add_source_keyboard())

    @dp.message_handler(commands=['see_my_sources'])
    async def see_my_sources(message: types.Message):
        users_sources = DatabaseCommunicator.sql_read_source(message.from_user.id)
        if len(users_sources) == 0:
            await message.answer(UserMessages.no_sources_mes)
        else:
            result = 'Вот список твоих источников: \n'
            for source in users_sources:
                result += source[1] + '\n'
            await message.answer(result, disable_web_page_preview=True)

    @dp.message_handler(commands=['delete_source'])
    async def delete_source(message: types.Message):
        sources = DatabaseCommunicator.sql_read_source(message.from_user.id)
        if len(sources) == 0:
            await message.answer(UserMessages.no_sources_mes)
        else:
            await message.answer(UserMessages.delete_source_mes,
                                 reply_markup=KeyboardCreator.delete_source_keyboard(sources))

    @dp.message_handler(commands=['parse'])
    async def choose_parse_time(message: types.Message):
        await message.answer(UserMessages.parse_time_mes, reply_markup=KeyboardCreator.parsing_time_keyboard())

    async def process_parse_command(call: types.CallbackQuery, parse_time):
        user = call["from"]["id"]
        users_sources = DatabaseCommunicator.sql_read_source(user)
        if len(users_sources) == 0:
            await call.message.answer(UserMessages.no_sources_mes)
        else:
            for source in users_sources:
                if source[2] == "vk":
                    await VkParser.parse_vk(source, user, parse_time)
                elif source[2] == "youtube":
                    await YoutubeParser.parse_youtube(source, user, parse_time)
                else:
                    print("Я пока не научился парсить источники такого типа")
            data = DatabaseCommunicator.sql_read_content(user)
            for post in data:
                if time.mktime(datetime.datetime.now().timetuple()) - int(post[6]) < int(parse_time):
                    mes_text = ((post[5] + '\n\n') if post[5] else '') + "Источник: " + post[4]
                    time.sleep(0.3)
                    mes = await call.message.answer(mes_text, disable_web_page_preview=False,
                                                    reply_markup=KeyboardCreator.channel_keyboard())
                    await DatabaseCommunicator.sql_add_message(post[0], mes["message_id"], user)

    @dp.message_handler()
    async def check_and_add(message: types.Message):
        has_moderated_channel = len(DatabaseCommunicator.sql_read_channel(message.from_user.id)) > 0
        if not has_moderated_channel:                            #на вход поступило название тг канала для модерации
            if message.forward_from_chat:
                await DatabaseCommunicator.sql_add_channel(message.from_user.id, message.forward_from_chat.title,
                                                           message.forward_from_chat.id)
                await message.answer(UserMessages.chan_success_mes)
            else:
                await message.answer(UserMessages.chan_mistake_mes)
        else:                                                       #на вход поступило название источника парсинга
            if validators.url(message.text):
                if len(message.text) > 15 and message.text[:15] == 'https://vk.com/':
                    await DatabaseCommunicator.sql_add_source(message.from_user.id, message.text, "vk")
                elif len(message.text) > 13 and message.text[:13] == 'https://t.me/':
                    await DatabaseCommunicator.sql_add_source(message.from_user.id, message.text, "tg")
                else:
                    await DatabaseCommunicator.sql_add_source(message.from_user.id, message.text, "youtube")
                await message.answer(UserMessages.url_success_mes)
            else:
                await message.answer(UserMessages.url_mistake_mes)

    @dp.callback_query_handler()
    async def process_answers(call: types.CallbackQuery):
        if call.data == "Телеграм канал/чат":
            await call.message.answer(UserMessages.add_tg_mes)
        elif call.data == "Сообщество VK":
            await call.message.answer(UserMessages.add_vk_mes)
        elif call.data == "Youtube канал":
            await call.message.answer(UserMessages.add_youtube_mes)
        elif call.data == "Установить канал":
            await call.message.answer(UserMessages.set_channel_mes_3)
        elif call.data == "Установить новый канал":
            DatabaseCommunicator.sql_delete_channel(call.from_user.id)
            await call.message.answer(UserMessages.set_channel_mes_3)
        elif call.data == "Оставить текущий":
            await call.message.answer("Окей")
        elif call.data[:4] == "dels":                                                       #delete_source
            DatabaseCommunicator.sql_delete_source(call["from"]["id"], call.data[4:])
            await call.message.answer(UserMessages.source_del_suc_mes)
        elif call.data[:4] == "delc":                                                       #delete content
            DatabaseCommunicator.sql_delete_message(call["from"]["id"], call.message.message_id)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        elif call.data == "Хочу выложить это в канал":
            chat_id = DatabaseCommunicator.sql_read_channel(call["from"]["id"])
            await ChannelCommunicator.send_message(chat_id[0][2], call.message.text)
        elif call.data.isdigit():
            await UserCommunicator.process_parse_command(call, call.data)
