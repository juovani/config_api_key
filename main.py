import requests
from configparser import ConfigParser


class NoSuchLocation(Exception):
    pass


location_input = input("enter zip here: ")


def get_location():
    location_url = 'https://dataservice.accuweather.com/locations/v1/' \
                f'postalcodes/search?apikey={api_key}&q={location_input}'
    response = requests.get(location_url)
    try:
        key = response.json()[0].get('Key')
    except IndexError:
        raise NoSuchLocation()
    return key


def get_conditions(key):
    conditions_url = 'https://dataservice.accuweather.com/currentconditions/v1/{}' \
        f'?apikey={api_key}'.format(key)
    response = requests.get(conditions_url)
    json_version = response.json()
    print("Current Conditions: {}".format(json_version[0].get('WeatherText')))


def get_temperature(key):
    temperature_url = 'https://dataservice.accuweather.com/currentconditions/v1/{}' \
        f'?apikey={api_key}'.format(key)
    response = requests.get(temperature_url)
    json_version = response.json()
    print("Current Temperature: {}".format(json_version[0]['Temperature']['Imperial']['Value'], 'f'))


def get_5dayforecast(key):
    forecast_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{}' \
                     f'?apikey={api_key}'.format(key)
    response = requests.get(forecast_url)
    json_version = response.json()
    days = json_version['DailyForecasts']
    for i in days:
        print(i['Date'])
        print('The Temperature is:', i['Temperature']['Maximum']['Value'],
              "Conditions: ", i['Day']['IconPhrase'])


def read_configfile():
    file = 'app.config'
    config = ConfigParser()
    config.read(file)
    api = config['secret']['apikey']
    # print(config['API']['API_Key'])

    return api


try:
    api_key = read_configfile()
    location_key = get_location()
    get_conditions(location_key)
    get_temperature(location_key)
    get_5dayforecast(location_key)
except NoSuchLocation:
    print("Unable to get the location")






