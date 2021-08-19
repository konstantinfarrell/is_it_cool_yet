import time
import os
import requests
import yaml

from twilio.rest import Client


with open('config.yaml', 'r') as stream:
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
    response = requests.get(WEATHER_URL)
    result = response.json()
    return result['main']['temp']


def send_alert():
    for person in SEND_TO:
        message = client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            body='open the window! it\'s cool out!',
            to=person)


def main():
    alert_when_below = False
    while True:
        temp = ping_weather()
        if temp > HEAT_THRESHOLD and alert_when_below == False:
            alert_when_below = True
        if alert_when_below == True and temp < COLD_THRESHOLD:
            send_alert()
            alert_when_below = False
        time.sleep(30)


if __name__ == '__main__':
    main()
