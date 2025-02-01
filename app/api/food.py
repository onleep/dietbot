import aiohttp
from dotenv import dotenv_values
from tools.logger import logging

URL = f'https://trackapi.nutritionix.com/v2/natural/nutrients'
env = dotenv_values()
headers = {
    'x-app-id': env.get('FOOD_APPID'),
    'x-app-key': env.get('FOOD_KEY'),
    'Content-Type': 'application/json'
}


async def get_kcal(product_name):
    data = {'query': product_name}

    async with aiohttp.ClientSession() as session:
        try:
            response = await session.post(URL, json=data, headers=headers)
            response.raise_for_status()
            data = await response.json()
        except Exception as e: 
            logging.error(str(e))
            return
        if 'foods' in data and len(data['foods']) > 0:
            calories = data['foods'][0].get('nf_calories')
            grams = data['foods'][0].get('serving_weight_grams')
            if not calories or not grams: return
            calories_100g = int(100 * calories / grams)
            return calories_100g
        return
