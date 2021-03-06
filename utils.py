import unicodedata
from collections import namedtuple
queries = {
    "forecast": "forecast",
    "location": "geolookup"
}
forecast_body = {'simplified': ("forecast", "simpleforecast", 'forecastday'),
                 'full': ("forecast", "txt_forecast", 'forecastday')
                 }
wind_directions = {
    '': 'North',
    'ENE': 'East-northeast',
    'ESE': 'East-southeast',
    'NE': 'Northeast',
    'NNE': 'North-northeast',
    'NNW': 'North-northwest',
    'North': 'North',
    'NW': 'Northwest',
    'SE': 'Southeast',
    'South': 'South',
    'SSE': 'South-southeast',
    'SSW': 'South-southwest',
    'SW': 'Southwest',
    'Variable': 'Variable',
    'West': 'West',
    'WNW': 'West-northwest',
    'WSW': 'West-southwest',
    'S': 'South',
    'N': 'North',
    'W': 'West',
    'E': 'East'

}

pretty_symbols = {
    "Rain": unicodedata.lookup("rain"),
    "Snow": unicodedata.lookup("snowflake"),
    "Fog": unicodedata.lookup("Foggy"),
    "Mist": unicodedata.lookup("Foggy"),
    "Cloudy": unicodedata.lookup("Cloud"),
    "Clear": unicodedata.lookup("Cloud"),
}


def sum_up_method(*args):
    return "".join(args)

CityInfo = namedtuple("CityInfo", ["name", "c_c"])
