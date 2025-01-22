from datetime import datetime

import buttons
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from tools.graphs import progress
from tools.utils import is_today

mainpage = Router()


@mainpage.message(Command('start'))
@mainpage.callback_query(F.data == 'main')
async def start_command(req: Message | CallbackQuery):
    message = req
    if isinstance(req, CallbackQuery):
        if not (message := req.message): return
        await req.answer()
    if (
        isinstance(message, Message)
        and (i := message.from_user)
        and i.is_bot
        and not message.photo
    ): method = message.edit_text
    else: method = message.answer
    slogans = [
        'Новый день — новые цели, где каждый день важен!',
        'Каждый шаг к здоровью — это шаг к новой версии себя!',
        'Баланс и результат — всё в твоих руках!',
        'Планируй, тренируйся, верь себя — достигай целей!',
    ]
    random = hash(datetime.now()) % len(slogans)
    await method(text=slogans[random], reply_markup=buttons.main)


@mainpage.message(Command('set_profile'))
@mainpage.callback_query(F.data == 'set_profile')
async def set_profile(req: Message | CallbackQuery, state: FSMContext):
    message = req
    if isinstance(req, CallbackQuery):
        if not (message := req.message): return
        await req.answer()
    data = await state.get_data()
    if not data or data.get('calories_goal') is None:
        profile = 'Не настроен'
    else:
        profile = (f"- Возраст: {data['age']}\n"
                   f"- Город: {data['city']}\n"
                   f"- Вес: {data['weight']} кг\n"
                   f"- Рост: {data['height']} см\n"
                   f"- Активность: {data['activity']}\n"
                   f"- Цель воды: {data['water_goal']} мл\n"
                   f"- Цель: {data['calories_goal']} ккал")
    if isinstance(message, Message) and (i := message.from_user) and i.is_bot:
        method = message.edit_text
    else: method = message.answer
    await method(f'⚙️ Текущий профиль:\n{profile}', reply_markup=buttons.set_profile)


@mainpage.message(Command('check_progress'))
@mainpage.callback_query(F.data == 'check_progress')
async def check_progress(req: Message | CallbackQuery, state: FSMContext):
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

    datenow = datetime.now().strftime(f'%Y-%m-%d')
    logged_water = await is_today(data, 'logged_water')
    logged_calories = await is_today(data, 'logged_calories')
    burned_calories = await is_today(data, 'burned_calories')

    if (wdg := data.get('water_daygoal')) and datenow in wdg:
        data['water_goal'] = wdg[datenow]
    left_water = (wg := data['water_goal']) - logged_water
    wat_asw = f'Осталось: {left_water} мл' if left_water > 0 else 'Вы выполнили норму'

    left_calories = logged_calories - burned_calories
    sum_calories = int(data['calories_goal'] + burned_calories * 0.5)
    cal_asw = (f'Баланс: {left_calories}'
               if logged_calories < sum_calories else 'Вы выполнили норму')

    high_temp = f'🥵 +500мл мл из-за жаркой погоды\n' if wdg and datenow in wdg else ''
    progress = (f'{high_temp}'
                f'💧 Вода:\n'
                f'- Сегодня выпито: {logged_water} мл из {wg}\n'
                f'- {wat_asw}\n\n'
                f'🔥 Калории:\n'
                f'- Потреблено: {logged_calories} ккал из {sum_calories}\n'
                f'- Сожжено: {burned_calories}\n'
                f'- {cal_asw}\n')
    await method(progress, reply_markup=buttons.progress)


@mainpage.callback_query(F.data == 'graph')
async def graph(req: CallbackQuery, state: FSMContext):
    if not (msg := req.message): return
    await req.answer()
    if isinstance(msg, Message) and (i := msg.from_user) and i.is_bot:
        method = msg.edit_text
    else: method = msg.answer
    data = await state.get_data()
    if data.get('calories_goal') is None:
        await method(f'⚙️ Профиль не настроен', reply_markup=buttons.set_profile)
        return
    if not (lw := data.get('logged_water')) or not (lc := data.get('logged_calories')):
        text = 'Калории или вода не были потреблены'
        await method(text, reply_markup=buttons.go_back)
        return
    progress_graph = await progress(lw, lc)
    file = BufferedInputFile(progress_graph, filename='graph.png')
    caption = '📊 График вашей диеты по дням'
    await msg.answer_photo(file, caption=caption, reply_markup=buttons.go_back)
