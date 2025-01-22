import buttons
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from routers.mainpage import set_profile
from states import User
from tools.utils import cities, validate_int

profiles = Router()


@profiles.callback_query(F.data == 'setprofile')
async def setprofile(callback: CallbackQuery, state: FSMContext):
    if not (msg := callback.message): return
    await state.clear()
    await msg.answer('🎂 Введите ваш возраст:')
    await callback.answer()
    await state.set_state(User.age)


@profiles.message(User.age)
async def age(message: Message, state: FSMContext):
    msg = await validate_int(message, 10, 100, 'Возраст')
    if isinstance(msg, Exception):
        await message.answer(str(msg))
        return
    await state.update_data(age=msg)
    text = '🌆 В каком городе вы находитесь?'
    await message.answer(text, reply_markup=buttons.cities_link)
    await state.set_state(User.city)


@profiles.message(User.city)
async def city(message: Message, state: FSMContext):
    if message.text not in cities:
        text = '🌆 Выберите верный город из списка'
        await message.answer(text, reply_markup=buttons.cities_link)
        return
    await state.update_data(city=message.text)
    await message.answer('⚖️ Введите ваш вес (в кг):')
    await state.set_state(User.weight)


@profiles.message(User.weight)
async def weight(message: Message, state: FSMContext):
    msg = await validate_int(message, 40, 250, 'Вес')
    if isinstance(msg, Exception):
        await message.answer(str(msg))
        return
    await state.update_data(water_goal=msg * 30)
    await state.update_data(weight=msg)
    await message.answer('📏 Введите ваш рост (в см):')
    await state.set_state(User.height)


@profiles.message(User.height)
async def height(message: Message, state: FSMContext):
    msg = await validate_int(message, 100, 250, 'Рост')
    if isinstance(msg, Exception):
        await message.answer(str(msg))
        return
    await state.update_data(height=msg)
    text = '🏃‍♂️ Выберите вашу активность'
    await message.answer(text, reply_markup=buttons.activity)
    await state.set_state(User.activity)


# @profiles.message(User.activity)
@profiles.callback_query(F.data.in_(['low', 'avg', 'high']))
async def activity(req: CallbackQuery, state: FSMContext):
    if not (msg := req.message): return
    await state.update_data(activity=req.data)
    await req.answer()
    method = msg.answer
    if isinstance(msg, Message) and (i := msg.from_user) and i.is_bot:
        method = msg.edit_text
    await method('🔥 Введите цель калорий', reply_markup=buttons.calories)
    await state.set_state(User.calories_goal)


@profiles.callback_query(F.data == 'calories')
async def calories_goals(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not callback.message: return
    message = callback.message
    if isinstance(message, Message) and (i := message.from_user) and i.is_bot:
        method = message.edit_text
    else: method = message.answer
    if not (activity := data.get('activity')): 
        await method(f'⚙️ Профиль не настроен', reply_markup=buttons.set_profile)
        return
    
    if activity == 'low': act_type = 1.2
    elif activity == 'avg': act_type = 1.5
    else: act_type = 1.7
    msg = 10 * data['weight'] + 6.25 * data['height'] - 5 * data['age'] + 5
    await state.update_data(calories_goal=int(msg * act_type))

    await callback.answer()
    await state.set_state(None)
    await set_profile(callback.message, state)


@profiles.message(User.calories_goal)
async def calories_goal(message: Message, state: FSMContext):
    msg = await validate_int(message, 1000, 5000, 'Цель калорий')
    if isinstance(msg, Exception):
        await message.answer(str(msg))
        return
    await state.update_data(calories_goal=msg)
    await state.set_state(None)
    await set_profile(message, state)
