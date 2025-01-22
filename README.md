# TG Бот для ведения диеты
https://github.com/user-attachments/assets/c3a2575a-c5e0-4761-bcb2-243b2d1acc7a

## Взаимодействие с сервисом
Реализован принцип взаимодействия работы с сервисом как используя команды, так и коллбеки. Методы полностью обратно заменяемы (повторяют функционал). Также при возможности бот редактирует сообщения, а не присылает всегда новые - что делает взаимодействие чистым.
```
В примерах задания использовались команды по типу /log_food apple 240, но тг команды не предназначены для такого взаимодействия. Это можно понять, выбрав команду из списка существующих команд в боте - она сразу же отправляется без возможности указать аргументы. Поэтому, мной был реализован общепринятый метод. Коллбек/команда -> Вопрос -> Ответ.
```

## Users states
Для хранения данных пользователей используется встроенный в aiogram [метод состояний](https://github.com/onleep/dietbot/blob/main/app/states.py). Который обеспечивает уникальные состояния и возможность взаимодействия с ними на ивентах.

## Профиль пользователя
Профиль пользователя состоит из 6 валидируемых вопросов. Реализован выбор активности из селекторов (низкая, средняя, высокая) и расчет необходимых воды + калорий на основе [формулы Миффлина-Сен Жеора](https://github.com/onleep/dietbot/blob/abc282e22b01c3ff5d74a0bbfa3892b742e71220/app/routers/profiles.py#L96) - что является общепринятной практикой.

## Учет воды, калорий и тренировок
- [Учет воды](https://github.com/onleep/dietbot/blob/abc282e22b01c3ff5d74a0bbfa3892b742e71220/app/routers/activity.py#L17): пользовтелю достаточно ввети потребленую воду в мл. При погоде 26+°C цель на день увеличивается на 500 мл.
 - [Учет калорий](https://github.com/onleep/dietbot/blob/abc282e22b01c3ff5d74a0bbfa3892b742e71220/app/routers/activity.py#L59): 1. Пользователь вводить название потребленной еды, происходит парсинг калорийности и ожидается ввод потребленный грамм. 2. Либо пользователь самостоятельно вводит число потребленных калорий.
 - [Учет тренировок](https://github.com/onleep/dietbot/blob/abc282e22b01c3ff5d74a0bbfa3892b742e71220/app/routers/activity.py#L115): пользователю предоставляется выбор из 3 тренировок (ходьба, бег, комплексная). В зависимости от типа [тренировки определяются](https://github.com/onleep/dietbot/blob/abc282e22b01c3ff5d74a0bbfa3892b742e71220/app/routers/activity.py#L144) сожженые калории + [прибавляется цель](https://github.com/onleep/dietbot/blob/abc282e22b01c3ff5d74a0bbfa3892b742e71220/app/routers/mainpage.py#L89) дневных ккал и [воды](https://github.com/onleep/dietbot/blob/abc282e22b01c3ff5d74a0bbfa3892b742e71220/app/routers/mainpage.py#L82).

## Работа с API
Реализована работа с двумя API.
- [OpenWeatherMap](https://github.com/onleep/dietbot/blob/main/app/api/temp.py) - сервис для парсинга погоды. При температуре выше 26°C, пользователю на определенный день повышается цель по потреблению воды.
- [Nutritionix](https://github.com/onleep/dietbot/blob/main/app/api/food.py) - сервис для парсинга калорийности еды. Сервис Nutritionix показывает себя лучше в определении калорийности еды и имеет адекватный API.

## Логирование
Реализовано [логирование ошибок](https://github.com/onleep/dietbot/blob/main/app/api/temp.py) при обращение к API. Также логируются все [команды и коллбеки](https://github.com/onleep/dietbot/blob/ef0e680130e0a5268250b00048edf3194ac93df6/app/tools/logger.py#L15) обращения к боту от пользователей +ошибки используя Middleware.

## Валидация данных
На каждом этапе ведения диеты валидируются данные на стороне приложения. Реализован [принцип приема](https://github.com/onleep/dietbot/blob/main/app/tools/utils.py) ожидаемой информации, а также выгружен список доступных городов для парсинга погоды.
