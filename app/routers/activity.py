from datetime import datetime

import buttons
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from api.food import get_kcal
from api.temp import get_temp
from routers.mainpage import check_progress
from states import User
from tools.utils import is_today, validate_int, prelogged

activity = Router()


@activity.message(Command('log_water'))
@activity.callback_query(F.data == 'log_water')
async def log_water(req: Message | CallbackQuery, state: FSMContext):
    message = req
    if isinstance(req, CallbackQuery):
        if not (message := req.message): return
        await req.answer()
    data = await state.get_data()
    if isinstance(message, Message) and (i := message.from_user) and i.is_bot:
        method = message.edit_text
    else:
        method = message.answer
    if data.get('calories_goal') is None:
        await method(f'⚙️ Профиль не настроен', reply_markup=buttons.set_profile)
        return
    await method('💧 Сколько вы выпили мл воды?', reply_markup=buttons.go_back)
    await state.set_state(User.logged_water)


@activity.message(User.logged_water)
async def logged_water(message: Message, state: FSMContext):
    msg = await validate_int(message, 1, 10000, 'Вода')
    if isinstance(msg, Exception):
        await message.answer(str(msg))
        return
    data = await state.get_data()
    datenow = datetime.now().strftime(f'%Y-%m-%d')

    if not datenow in data.get('weather_temp', {}):
        temp = await get_temp(data['city'])
        data['weather_temp'] = {datenow: temp}
        await state.update_data(weather_temp={datenow: temp})
        if temp and temp > 26:
            wgoal = await is_today(data, 'water_daygoal') or data['water_goal']
            water_daygoal = wgoal + 500
            await state.update_data(water_daygoal={datenow: water_daygoal})

    dtarget = await prelogged(data, 'logged_water', msg)
    await state.update_data(logged_water=dtarget)
    await state.set_state(None)
    await check_progress(message, state)


@activity.message(Command('log_food'))
@activity.callback_query(F.data == 'log_food')
async def log_food(req: Message | CallbackQuery, state: FSMContext):
    message = req
    if isinstance(req, CallbackQuery):
        if not (message := req.message): return
        await req.answer()
    data = await state.get_data()
    if isinstance(message, Message) and (i := message.from_user) and i.is_bot:
        method = message.edit_text
    else: method = message.answer

    if data.get('calories_goal') is None:
        await method(f'⚙️ Профиль не настроен', reply_markup=buttons.set_profile)
        return
    text = '🔥 Укажите кол-во ккал / название продукта'
    await method(text, reply_markup=buttons.food_log)
    await state.set_state(User.logged_calories)


async def update_callories(data: dict, state: FSMContext, message, msg):
    dtarget = await prelogged(data, 'logged_calories', msg)
    await state.update_data(logged_calories=dtarget)
    await state.set_state(None)
    await check_progress(message, state)


@activity.message(User.logged_calories)
async def logged_calories(message: Message, state: FSMContext):
    msg = await validate_int(message, 1, 10000, 'Калории')
    if isinstance(msg, Exception):
        kcal = await get_kcal(message.text)
        if not kcal:
            text = f'Введите верный продукт из списка или {msg}'
            await message.answer(text, reply_markup=buttons.food_log)
            return
        text = f'{message.text} — {kcal} ккал на 100 гр.\nСколько грамм вы съели?'
        await message.answer(text, reply_markup=buttons.go_back)
        await state.update_data(waited_calories=kcal)
        await state.set_state(User.waited_calories)
        return
    data = await state.get_data()
    await update_callories(data, state, message, msg)


@activity.message(User.waited_calories)
async def waited_calories(message: Message, state: FSMContext):
    msg = await validate_int(message, 10, 5000, 'Кол-во грамм')
    if isinstance(msg, Exception):
        await message.answer(str(msg))
        return
    data = await state.get_data()
    msg = int(data['waited_calories'] / 100 * msg)
    await update_callories(data, state, message, msg)


@activity.message(Command('log_workout'))
@activity.callback_query(F.data == 'log_workout')
async def log_workout(req: Message | CallbackQuery, state: FSMContext):
    message = req
    if isinstance(req, CallbackQuery):
        if not (message := req.message): return
        await req.answer()
    data = await state.get_data()
    if isinstance(message, Message) and (i := message.from_user) and i.is_bot:
        method = message.edit_text
    else: method = message.answer
    if data.get('calories_goal') is None:
        await method(f'⚙️ Профиль не настроен', reply_markup=buttons.set_profile)
        return
    await method('Выберите вид тренировки', reply_markup=buttons.log_train)


@activity.callback_query(F.data.in_(['walking', 'running', 'complex']))
async def set_workout(req: CallbackQuery, state: FSMContext):
    if not (msg := req.message): return
    await state.update_data(train_type=req.data)
    await req.answer()
    if isinstance(msg, Message) and (i := msg.from_user) and i.is_bot:
        method = msg.edit_text
    else: method = msg.answer
    await method('Сколько минут длилась тренировка?', reply_markup=buttons.go_back)
    await state.set_state(User.burned_calories)


@activity.message(User.burned_calories)
async def burned_calories(message: Message, state: FSMContext):
    msg = await validate_int(message, 1, 300, 'Минут')
    if isinstance(msg, Exception):
        await message.answer(str(msg))
        return
    data = await state.get_data()
    if (i := data['train_type']) == 'walking': train_load = 5
    elif i == 'running': train_load = 10
    else: train_load = 15
    msg = int(msg * train_load)
    datenow = datetime.now().strftime(f'%Y-%m-%d')
    burned_calories = await is_today(data, 'burned_calories') + msg
    wgoal = await is_today(data, 'water_daygoal') or data['water_goal']
    water_daygoal = wgoal + int(burned_calories * 1.2)
    await state.update_data(burned_calories={datenow: burned_calories})
    await state.update_data(water_daygoal={datenow: water_daygoal})
    await state.set_state(None)
    await check_progress(message, state)
