from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup

bot_commands = [
    BotCommand(command='/start', description='Запустить бота'),
    BotCommand(command='/set_profile', description='Настройка профиля'),
    BotCommand(command='/log_water', description='Указать выпитую воду'),
    BotCommand(command='/log_food', description='Указать потребленные ккал'),
    BotCommand(command='/log_workout', description='Указать тренировку'),
    BotCommand(command='/check_progress', description='Прогресс диеты'),
]

main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🔥 Указать калории', callback_data='log_food'),
        InlineKeyboardButton(text='💧 Указать воду', callback_data='log_water')
    ], [InlineKeyboardButton(text='💪 Указать тренировку', callback_data='log_workout')],
    [
        InlineKeyboardButton(text='📊 Прогресс диеты', callback_data='check_progress'),
        InlineKeyboardButton(text='⚙️ Профиль', callback_data='set_profile'),
    ]
])

set_profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Настроить профиль', callback_data='setprofile')],
    [InlineKeyboardButton(text='Вернуться назад', callback_data='main')],
])

log_train = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🚶‍♂️ Ходьба', callback_data='walking'),
        InlineKeyboardButton(text='🏃‍♂️ Бег', callback_data='running')
    ],
    [InlineKeyboardButton(text='🏋️‍♀️ Комплексная', callback_data='complex')],
    [InlineKeyboardButton(text='Вернуться назад', callback_data='main')],
])

calories = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Авторасчет', callback_data='calories'),
]])

activity = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Сижу дома', callback_data='low'),
        InlineKeyboardButton(text='Хожу в магазин', callback_data='avg')
    ],
    [InlineKeyboardButton(text='Занимаюсь спортом', callback_data='high')],
])

cities_link = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Список городов',
                         url='https://openweathermap.org/weathermap')
]])

food_log = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Список продуктов',
                             url='https://www.nutritionix.com/database')
    ],
    [InlineKeyboardButton(text='Вернуться назад', callback_data='main')],
])

progress = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть график', callback_data='graph')],
    [InlineKeyboardButton(text='Вернуться назад', callback_data='main')],
])

go_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться назад', callback_data='main')],
])
