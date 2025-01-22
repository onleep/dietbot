import aiohttp
from dotenv import dotenv_values
from tools.logger import logging

URL = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_KEY = dotenv_values().get('WEATHER_KEY')


async def get_temp(city):
    params = {'q': city, 'appid': WEATHER_KEY, 'units': 'metric'}
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get(URL, params=params)
            response.raise_for_status()
            data = await response.json()
        except Exception as e: 
            logging.error(str(e))
            return
        temp = data.get('main', {}).get('temp')
        return temp
