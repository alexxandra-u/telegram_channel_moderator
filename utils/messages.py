class UserMessages:
    start_mes = "Этот бот поможет тебе находить новый контент в ваших любимых источниках и делиться им в своем " \
                "телеграм канале. Чтобы начать пользоваться ботом, сделайте его админом со всеми правами в своем " \
                "телеграм-канале. После этого воспользуйтесь командой /set_channel"
    help_mes = 'Этот бот поможет находить новый контент в ваших любимых источниках и в пару кликов делиться' \
               ' им в вашем телеграм канале. Чтобы пользоваться ботом вам потребуется ваш телеграм-канал. ' \
               'Сделайте бота в нём администратором со всеми правами и переходите к команде /set_channel.' \
               '\n\nСправка о командах:\n\n' \
               '/start - начало работы\n' \
               '/help - справка о командах\n' \
               '/set_channel - установка канала для модерации\n' \
               '/add_new_sourse - добавление нового источника контента\n' \
               '/see_my_sources - просмотр текущих источников контента\n' \
               '/delete_source - удаление источника контента\n' \
               '/parse - получить новые посты из источников'
    source_choice_mes = "Выберите тип источника, который хочешь добавить, с помощью кнопок ниже"
    add_tg_mes = "Отправьте мне ссылку на нужный канал/чат в формате @name или https://t.me/name"
    add_vk_mes = "Отправьте мне ссылку на нужное сообщество в формате https://vk.com/name"
    add_youtube_mes = "Отправьте мне ссылку на нужный youtube калан в формате https://www.youtube.com/name"
    url_success_mes = "Отлично, новый источник был добавлен"
    no_channel_mes = "Пожалуйста, выбирите канал, который хотите модерировать, с помощью команды /set_channel ." \
                     " Без этого бот не сможет начать работу."
    chan_success_mes = "Отлично, канал для модерации был добавлен. Теперь вы можете добавлять ваши любимые источники " \
                       "контента с помощью команды /add_new_source"
    no_sources_mes = "Вы еще не добавили источники, из которых хотите получать информацию. Сделайте это с помощью " \
                     "команды /add_new_source "
    no_news_mes = '🤷🏻 По заданным вами параметрам не нашлось контента. Попробуйте выбрать больший временной промежуток ' \
                  'или другой тон для контента'
    delete_source_mes = "Выберите какой из источников вы хотите удалить"
    source_del_suc_mes = "Вы больше не будете получать контент из этого источника"
    chan_mistake_mes = "Кажется вы отправили что-то не то. Проверьте правильность и попробуйте еще раз."
    set_channel_mes_1 = "На данный момент вы модерируете канал "
    set_channel_mes_2 = "На данный момент у вас не установлен никакой канал для модерации"
    set_channel_mes_3 = "Перешлите мне любое сообщение из канала, который хотите модерировать. " \
                        "Не забудьте сделать этого бота админом со всеми правами в этом канале, иначе бот просто не " \
                        "сможет ничего туда выкладывать."
    parse_time_mes = "Выберите контент за какой срок вы хотите получить"
    edit_mes = "Отправьте мне исправленный текст сообщения. Чтобы не нарушать авторские права, " \
               "не меняйте текст больше чем на 10% и не удаляйте ссылку на источник"
    no_edit_mes = 'Вы поменяли текст больше чем на 10% или удалили ссылку на источник. Мы не можем сохранить пост в' \
                  ' таком виде. Попробуйте ещё раз.'
    choose_tone_message = 'Выберите, какой контент вы хотите получить'
    end_parsing_mes = ' ⬆️ Вот весь контент который мы нашли по вашему запросу ⬆️'
