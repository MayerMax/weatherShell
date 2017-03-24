import argparse
import urllib.request
import json
from utils import sum_up_method, queries, wind_directions
from utils import forecast_body as body

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

    def _raw_weather_response(self):
        res_string = sum_up_method(self.pattern_query,
                                   application_key,
                                   "/", queries["forecast"],
                                   "/q/", self.country, "/", self.city,
                                   ".json")

        with urllib.request.urlopen(res_string) as response:
            data = json.loads(response.read().decode())
            weather_info = self._body_wrap(*body["simplified"], data=data) \
                if self.simplified else self._body_wrap(*body["full"], data=data)

            for w in weather_info:
                print(w)

    @classmethod
    def _body_wrap(cls, *args, data):
        cur_dict = None
        for arg in args:
            if cur_dict is None:
                cur_dict = data[arg]
            else:
                cur_dict = cur_dict[arg]
        return cur_dict


class SimplifiedForecast:
    def __init__(self, weather_record):
        self.date = weather_record["date"]
        self.temp = (weather_record['low']['celsius'], weather_record['high']['celsius'])
        self.resume = weather_record['conditions']
        self.humidity = weather_record['avehumidity']
        self.wind_info = weather_record["maxwind"]

    def _wind_info_representation(self):
        return "Wind direction is " + wind_directions[self.wind_info['dir']] + \
               "speed is" + self.wind_info["kph"] + "kilometers per hour"

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


if __name__ == '__main__':
    parser = get_args_parser()
    q = QueryResponse()
    q._raw_weather_response()
    # q = QueryAutocomplete("yekater")
    # a = q.clarify_query()
    # print(a)
