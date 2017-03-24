import argparse
import urllib.request
import json
from utils import sum_up_method, queries, wind_directions

application_key = "dd2ea79e4555250f"


def get_args_parser():
    parser = argparse.ArgumentParser(description="Weather api tool")
    parser.add_argument("source",
                        help="Weather for given source City")

    parser.add_argument("region",
                        help="type a country to specify the search",
                        default="RU", type=str)


class QueryResponse:
    def __init__(self, country="Ru", city="Yekaterinburg",
                 version="simplified", days=1):
        self.clarification = None
        self.country = country
        self.city = city
        self.version = version
        self.pattern_query = "http://api.wunderground.com/api/"
        self.days = days

    def _raw_weather_response(self):
        res_string = sum_up_method(self.pattern_query,
                                   application_key,
                                   "/", queries["forecast"],
                                   "/q/", self.country, "/", self.city,
                                   ".json")

        with urllib.request.urlopen(res_string) as response:
            data = response.read().decode()
            weather_info = json.loads(data)["forecast"]["simpleforecast"][
                'forecastday']
            for w in weather_info:
                print(w)


class SimplifiedForecast:
    def __init__(self, weather_record):
        self.date = weather_record["date"]
        self.temp = (weather_record['low']['celsius'],
                     weather_record['high']['celsius'])
        self.resume = weather_record['conditions']
        self.humidity = weather_record['avehumidity']
        self.wind_info = weather_record["maxwind"]

    def _wind_info_representation(self):
        return "Wind direction is " \
               + wind_directions[self.wind_info['dir']] + "speed is" + \
               self.wind_info["kph"] + "kilometers per hour"

    def prepare_representation(self):
        pass

class QueryAutocomplete:
    def __init__(self, given_name):
        self.given_name = given_name
        self.pattern_query = "http://autocomplete.wunderground.com/aq?query="

    def clarify_query(self):
        res_string = sum_up_method(self.pattern_query, self.given_name)

        with urllib.request.urlopen(res_string) as response:
            data = response.read().decode()
            city_info = json.loads(data)["RESULTS"]
            for city in city_info:
                if city['name'] == self.given_name:
                    return city

            return city_info


q = QueryResponse()
q._raw_weather_response()
# q = QueryAutocomplete("yekater")
# a = q.clarify_query()
# print(a)
