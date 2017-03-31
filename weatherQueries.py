import argparse
import urllib.request
import json
from ForecastTemplates import SimplifiedForecast, FullForecast
from utils import sum_up_method, queries, wind_directions
from utils import forecast_body as body, pretty_symbols as symbols
from utils import CityInfo
from support_handlers import *

application_key = "dd2ea79e4555250f"  # my temporary key for api on wunderground.com


def get_args_parser():
    arg_parser = argparse.ArgumentParser(description="Weather api tool")
    arg_parser.add_argument("source", help="Weather for given source City")

    arg_parser.add_argument("region", help="type a country to specify the search",
                            default="RU", type=str)
    return arg_parser


class QueryResponse:
    def __init__(self, country="Ru", city="Yekaterinburg",
                 simplified=False, days=1):
        self.clarification = None
        self.country = country
        self.city = city
        self.simplified = simplified
        self.pattern_query = "http://api.wunderground.com/api/"
        self.days = days

    def make_forecast(self):
        return self._raw_weather_response()

    def _raw_weather_response(self):
        res_string = sum_up_method(self.pattern_query,
                                   application_key,
                                   "/", queries["forecast"],
                                   "/q/", self.country, "/", self.city,
                                   ".json")

        with urllib.request.urlopen(res_string) as response:
            data = json.loads(response.read().decode())
            if self.simplified:
                info = SimplifiedForecast.wrap(self._body_wrap(*body["simplified"],
                                                               data=data))
            else:
                info = FullForecast.wrap(self._body_wrap(*body["full"], data=data))
        return info

    @classmethod
    def _body_wrap(cls, *args, data):
        cur_dict = None
        for arg in args:
            if cur_dict is None:
                cur_dict = data[arg]
            else:
                cur_dict = cur_dict[arg]
        return cur_dict




class QueryAutocomplete:
    def __init__(self, given_name):
        self.given_name = assert_ascii(given_name)
        self.pattern_query = "http://autocomplete.wunderground.com/aq?query="

    def clarify_query(self):
        res_string = sum_up_method(self.pattern_query, self.given_name)

        with urllib.request.urlopen(res_string) as response:
            data = response.read().decode()
            city_info = json.loads(data)["RESULTS"]
            for city in city_info:
                if city['name'][0:city['name'].index(',')] in self.given_name:
                    return city

            return city_info


def weather_query(city):
    query = QueryAutocomplete(city)
    query_info = query.clarify_query()
    if isinstance(query_info, list) and len(query_info) > 0:
        possible_values = []
        for q in query_info:
            possible_values.append(CityInfo(q['name'], q['c']))
        print_auto_complete_variants(possible_values)

        while True:
            city = input()
            weather_query(city)
            break
    elif isinstance(query_info, dict):
        req = CityInfo(query_info['name'][0:query_info['name'].index(',')],
                       query_info['c'])
        forecast = QueryResponse(country=req.c_c, city=req.name).make_forecast()
        for f in forecast:
            print(f)
            break


if __name__ == '__main__':
    parser = get_args_parser()
    # q = QueryResponse()
    # q._raw_weather_response()
    weather_query("Yekaterinburg")
