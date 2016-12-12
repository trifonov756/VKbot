import vk
import time
import datetime

from OpenWeatherMap import translate_city, location, cloudiness
from OpenWeatherMap import weather

session = vk.Session('b005b12df347bb609eb8b487ff6651a80a893c98b66f1ec3011e9cae9c1ccf3f8086edbf0f9e06c6a56ed')

api = vk.API(session)

while True:

    messages = api.messages.get()

    commands = [ 'help', 'weather']

    messages = [(m['uid'], m['mid'], m['body'])
                for m in messages[1:] if m['body'] in commands and m['read_state'] == 0]

    for m in messages:
        user_id = m[0]
        message_id = m[1]
        command = m[2]

        date_time_string = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

        if command == 'help':
            api.messages.send(user_id=user_id,
                              message=date_time_string + '\n>VKBot v0.1\n>Разработал: Elagin')

        if command == 'weather':
            api.messages.send(user_id=user_id,
                              message=('Погода в городе ' + translate_city[location.get_name()] + ' (' + translate_country[location.get_country()] +
    ') ' + 'на сегодня ' + str(datetime.now().strftime("%H:%M")) + ' ' + cloudiness() + ',облачность составляет ' +
    str(weather.get_clouds()) + ' %, давление ' + str(round(weather.get_pressure()['press'] * 0.750062)) +
    ' мм рт. ст.,макс температура ' + str(weather.get_temperature('celsius')['temp_max']) + ' мин температура'
    + str(weather.get_temperature('celsius')['temp_min']) + ' градусов Цельция' + ', ветер ' + str(round(weather.get_wind()['speed'])) + ' м/c'))

    ids = ', '.join([str(m[1]) for m in messages])

    if ids:
        api.messages.markAsRead(message_ids=ids)

time.sleep(3)