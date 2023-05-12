from aiogram import types
from aiogram.utils.exceptions import CantParseEntities
from create_bot import bot, dp
from parsers.vk_parser import VkParser
from parsers.youtube_parser import YoutubeParser
from parsers.tg_parser import TgParser
from handlers.database_communicator import DatabaseCommunicator
from handlers.channel_communicator import ChannelCommunicator
from utils.keyboards import KeyboardCreator
from utils.messages import UserMessages
import time
import datetime
import difflib


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
            await message.answer(UserMessages.set_channel_mes_1 + '*' + channel[0][1] + '*',
                                 reply_markup=KeyboardCreator.reset_channel_keyboard(), parse_mode='Markdown')

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

    async def choose_tone(call: types.CallbackQuery, parse_time):
        await call.message.answer(UserMessages.choose_tone_message,
                                  reply_markup=KeyboardCreator.parsing_tone_keyboard(parse_time))

    async def process_parse_command(call: types.CallbackQuery, tone, parse_time):
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
                elif source[2] == "tg":
                    await TgParser.parse_tg(source, user, parse_time)
                else:
                    print("Я пока не научился парсить источники такого типа")
            data = DatabaseCommunicator.sql_read_content(user)
            toned_data = DatabaseCommunicator.sql_read_tone_content(user, tone)
            if len(data) == 0 or (tone != 'all' and len(toned_data) == 0):
                await call.message.answer(UserMessages.no_news_mes)
            for post in data:
                if time.mktime(datetime.datetime.now().timetuple()) - int(post[6]) < int(parse_time) and (tone == 'all'
                                                                                                          or tone ==
                                                                                                          post[7]):
                    mes_base = (post[5] + '\n\n') if post[5] else ''
                    time.sleep(0.3)
                    if post[2] == 'tg' and 'реклама' not in mes_base:
                        try:
                            mes_text = mes_base + "Источник: [" + post[4] + '](' + post[4] + ')'
                            mes = await call.message.answer(mes_text, disable_web_page_preview=True,
                                                            parse_mode='Markdown',
                                                            reply_markup=KeyboardCreator.channel_keyboard())
                        except CantParseEntities:
                            mes_text = mes_base + "Источник: " + post[4]
                            mes = await call.message.answer(mes_text, disable_web_page_preview=True,
                                                            reply_markup=KeyboardCreator.channel_keyboard())
                        await DatabaseCommunicator.sql_add_message(post[0], mes["message_id"], user)
                    elif 'реклама' not in mes_base:
                        mes_text = mes_base + "Источник: " + post[4]
                        mes = await call.message.answer(mes_text, disable_web_page_preview=False,
                                                        reply_markup=KeyboardCreator.channel_keyboard())
                        await DatabaseCommunicator.sql_add_message(post[0], mes["message_id"], user)
                elif time.mktime(datetime.datetime.now().timetuple()) - int(post[6]) > 604800:
                    DatabaseCommunicator.sql_delete_content(post[1], post[0])

    def compare_texts(old_text, new_text):
        normalized1 = old_text.lower()
        normalized2 = new_text.lower()
        matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
        return matcher.ratio()

    @dp.message_handler()
    async def process_other_messages(message: types.Message):
        has_moderated_channel = len(DatabaseCommunicator.sql_read_channel(message.from_user.id)) > 0
        if not has_moderated_channel:                            # на вход поступило название тг канала для модерации
            if message.forward_from_chat:
                await DatabaseCommunicator.sql_add_channel(message.from_user.id, message.forward_from_chat.title,
                                                               message.forward_from_chat.id)
                await message.answer(UserMessages.chan_success_mes)
            else:
                await message.answer(UserMessages.chan_mistake_mes)
        else:                                   # на вход поступило название источника парсинга или новый текст
            if len(message.text) > 15 and message.text[:15] == 'https://vk.com/':
                await DatabaseCommunicator.sql_add_source(message.from_user.id, message.text, "vk")
                await message.answer(UserMessages.url_success_mes)
            elif message.text[0] == "@" or (len(message.text) > 13 and message.text[:13] == 'https://t.me/'):
                await DatabaseCommunicator.sql_add_source(message.from_user.id, message.text, "tg")
                await message.answer(UserMessages.url_success_mes)
            elif len(message.text) > 24 and message.text[:24] == 'https://www.youtube.com/':
                await DatabaseCommunicator.sql_add_source(message.from_user.id, message.text, "youtube")
                await message.answer(UserMessages.url_success_mes)
            else:
                old_text = DatabaseCommunicator.sql_read_content_in_process(message.from_user.id)[2]
                content_id = DatabaseCommunicator.sql_read_content_in_process(message.from_user.id)[0]
                start_index = old_text.find("Источник: ")
                source_link = old_text[start_index:]
                ratio = UserCommunicator.compare_texts(message.text, old_text)
                if ratio >= 0.9 and source_link in message.text:
                    await DatabaseCommunicator.sql_edit_content(message.from_user.id, old_text, message.text)
                    try:
                        mes = await message.answer(message.text, disable_web_page_preview=True, parse_mode='Markdown',
                                                   reply_markup=KeyboardCreator.channel_keyboard())
                    except CantParseEntities:
                        mes = await message.answer(message.text, disable_web_page_preview=True,
                                                   reply_markup=KeyboardCreator.channel_keyboard())
                    await DatabaseCommunicator.sql_add_message(content_id, mes["message_id"], message.from_user.id)
                else:
                    await message.answer(UserMessages.no_edit_mes)

    @dp.callback_query_handler()
    async def process_answers(call: types.CallbackQuery):
        # source choosing
        if call.data == "Телеграм канал/чат":
            await call.message.answer(UserMessages.add_tg_mes)
        elif call.data == "Сообщество VK":
            await call.message.answer(UserMessages.add_vk_mes)
        elif call.data == "Youtube канал":
            await call.message.answer(UserMessages.add_youtube_mes)

        # channel setting
        elif call.data == "Установить канал":
            await call.message.answer(UserMessages.set_channel_mes_3)
        elif call.data == "Установить новый канал":
            DatabaseCommunicator.sql_delete_channel(call.from_user.id)
            await call.message.answer(UserMessages.set_channel_mes_3)
        elif call.data == "Оставить текущий канал":
            await call.message.answer("Окей")

        # tone choosing
        elif call.data[:3] in ["all", "pos", "neu", "neg"]:
            await UserCommunicator.process_parse_command(call, call.data[:3], call.data[3:])

        elif call.data[:4] == "dels":                                                       # delete_source
            DatabaseCommunicator.sql_delete_source(call["from"]["id"], call.data[4:])
            await call.message.answer(UserMessages.source_del_suc_mes)
        elif call.data[:4] == "delc":                                                       # delete content
            DatabaseCommunicator.sql_delete_message(call["from"]["id"], call.message.message_id)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        elif call.data == 'edit':
            content_id = DatabaseCommunicator.sql_read_spes_content(call.from_user.id, call.message.text)[0]
            await DatabaseCommunicator.sql_change_content_in_process(call.message.text, call.from_user.id, content_id)
            await call.message.answer(UserMessages.edit_mes)
        elif call.data == "Выложить в канал":
            chat_id = DatabaseCommunicator.sql_read_channel(call["from"]["id"])
            await ChannelCommunicator.send_message(chat_id[0][2], call.message.text)
        elif call.data.isdigit():
            await UserCommunicator.choose_tone(call, call.data)
