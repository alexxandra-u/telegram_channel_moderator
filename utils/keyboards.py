from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardCreator():
    def add_source_keyboard():
        inline_keyboard = InlineKeyboardMarkup()
        buttons_text = ["Телеграм канал/чат", "Сообщество VK", "Youtube канал"]
        for i in range(len(buttons_text)):
            btn = InlineKeyboardButton(buttons_text[i], callback_data=buttons_text[i])
            inline_keyboard.add(btn)
        return inline_keyboard

    def delete_source_keyboard(sources):
        inline_keyboard = InlineKeyboardMarkup()
        for source in sources:
            btn = InlineKeyboardButton(source[1], callback_data="dels" + source[1])
            inline_keyboard.add(btn)
        return inline_keyboard

    def set_channel_keyboard():
        inline_keyboard = InlineKeyboardMarkup()
        btn = InlineKeyboardButton("Установить канал", callback_data="Установить канал")
        inline_keyboard.add(btn)
        return inline_keyboard

    def reset_channel_keyboard():
        inline_keyboard = InlineKeyboardMarkup()
        buttons_text = ["Оставить текущий канал", "Установить новый канал"]
        for i in range(len(buttons_text)):
            btn = InlineKeyboardButton(buttons_text[i], callback_data=buttons_text[i])
            inline_keyboard.add(btn)
        return inline_keyboard

    def channel_keyboard():
        inline_keyboard = InlineKeyboardMarkup()
        buttons_text = ["Выложить в канал", "Отредактировать текст", "Удалить"]
        btn1 = InlineKeyboardButton(buttons_text[0], callback_data=buttons_text[0])
        btn2 = InlineKeyboardButton(buttons_text[1], callback_data='edit')
        btn3 = InlineKeyboardButton(buttons_text[2], callback_data='delc' + buttons_text[2])
        inline_keyboard.add(btn1)
        inline_keyboard.add(btn2)
        inline_keyboard.add(btn3)
        return inline_keyboard

    def parsing_time_keyboard():
        inline_keyboard = InlineKeyboardMarkup()
        buttons_text = ["12 часов", "1 день", "2 дня", "3 дня", "1 неделя"]
        buttons_callback = ["43200", "86400", "172800", "259200", "604800"]
        for i in range(len(buttons_text)):
            btn = InlineKeyboardButton(buttons_text[i], callback_data=buttons_callback[i])
            inline_keyboard.add(btn)
        return inline_keyboard

    def parsing_tone_keyboard(parsing_time):
        inline_keyboard = InlineKeyboardMarkup()
        buttons_text = ["Весь", "Только позитивный", "Только нейтральный", "Только негативный"]
        buttons_callback = ['all', 'pos', 'neu', 'neg']
        for i in range(len(buttons_text)):
            btn = InlineKeyboardButton(buttons_text[i], callback_data=buttons_callback[i] + parsing_time)
            inline_keyboard.add(btn)
        return inline_keyboard

