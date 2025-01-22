import json
from datetime import datetime

from aiogram.types import Message


async def validate_int(message: Message, min_value: int, max_value: int,
                       target: str) -> int | Exception | ValueError:
    if not (msg := message.text):
        return Exception(f'Сообщение не найдено')
    if not msg.isdigit():
        return Exception(f'{target} должен быть целым числом')
    if not min_value <= (msg := int(msg)) <= max_value:
        return Exception(f'Введите {target.lower()} от {min_value} до {max_value}')
    return msg


async def prelogged(data: dict, target: str, upd: int = False) -> list:
    datenow = datetime.now().strftime(f'%Y-%m-%d')
    if not (dtarget := data.get(target, [])) or datenow not in dtarget[-1]:
        dtarget.append({datenow: 0})
    if upd: dtarget[-1][datenow] += upd
    return dtarget[-7:] # last week


async def is_today(data: dict, target: str) -> int:
    datenow = datetime.now().strftime(f'%Y-%m-%d')
    if target in ('logged_calories', 'logged_water'):
        if not (data_target := data.get(target, [])):
            return 0
        data_target = data_target[-1]
    else: data_target = data.get(target, {})
    
    if datenow not in data_target:
        data_target = {datenow: 0}
    return data_target[datenow]


def get_cities() -> set[str]:
    with open('app/tools/city_list.json', 'r', encoding='utf-8') as f:
        raw_cities = json.load(f)
    cities = set()
    for city in raw_cities:
        if not city.get('name'): continue
        cities.add(city['name'])
    return cities


cities = get_cities()
