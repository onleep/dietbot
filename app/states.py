from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    age = State()
    city = State()
    weight = State()
    height = State()
    activity = State()

    water_goal = State()
    logged_water = State()
    water_daygoal = State()

    calories_goal = State()
    logged_calories = State()
    burned_calories = State()
    waited_calories = State()

    train_type = State()

    weather_temp = State()
