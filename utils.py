queries = {
    "forecast": "forecast",
    "location": "geolookup"
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
    'WSW': 'West-southwest'

}


def sum_up_method(*args):
    return "".join(args)
