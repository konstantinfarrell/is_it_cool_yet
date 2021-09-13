import time
import os
import requests
import yaml

from twilio.rest import Client


cfg = 'config.yaml'
with open(cfg, 'r') as stream:
    config = yaml.safe_load(stream)


CITY = config['city']
STATE = config['state']
COUNTRY = config['country']

HEAT_THRESHOLD = config['heat_threshold']
COLD_THRESHOLD = config['cold_threshold']

WEATHER_API_TOKEN = config['weather_api_token']
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY},{STATE},{COUNTRY}&appid={WEATHER_API_TOKEN}&units=imperial'


t = config['twilio']
TWILIO_SID = t['sid']
TWILIO_AUTH_TOKEN = t['auth_token']
TWILIO_PHONE_NUMBER = t['phone_number']

SEND_TO = config['numbers']


client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


def ping_weather():
    try:
        response = requests.get(WEATHER_URL)
    except Exception:
        return None
    result = response.json()
    return result['main']['temp']

def send_alert(message):
    for person in SEND_TO:
        result = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            body=message,
            to=person)


def main():
    alert_when_below = False
    while True:
        wait = 60
        temp = ping_weather()
        if not temp:
            print('no response. sleeping')
            time.sleep(wait * 3)
            continue
        if temp > HEAT_THRESHOLD and alert_when_below == False:
            alert_when_below = True
        if alert_when_below == True and temp < COLD_THRESHOLD:
            send_alert('\nOpen the window! It\'s cool out!')
            alert_when_below = False
            wait = 3600 * 12
            print('sleeping for the night')
        print('.', end='')
        time.sleep(wait)


if __name__ == '__main__':
    main()
