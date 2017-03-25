import argparse
import urllib.request
import json
from utils import sum_up_method, queries, wind_directions
from utils import forecast_body as body, pretty_symbols as symbols
from utils import CityInfo

application_key = "dd2ea79e4555250f"  # my temporary key for api on wunderground.com


def get_args_parser():
    arg_parser = argparse.ArgumentParser(description="Weather api tool")
    arg_parser.add_argument("source", help="Weather for given source City")

    arg_parser.add_argument("region", help="type a country to specify the search",
                            default="RU", type=str)
    return arg_parser


class QueryResponse:
    def __init__(self, country="Ru", city="Yekaterinburg",
                 simplified=True, days=1):
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
            if self.simplified:
                info = SimplifiedForecast.wrap(self._body_wrap(*body["simplified"],
                                                               data=data))
            else:
                info = FullForecast.wrap(self._body_wrap(*body["full"], data=data))

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
               " and speed is " + str(self.wind_info["kph"]) + " kilometers per hour\n"

    @staticmethod
    def wrap(weather_records):
        all_records = []
        for record in weather_records:
            all_records.append(SimplifiedForecast(record))
        return all_records

    def __str__(self):
        return "Date is " + self.date['pretty'] + ", " + self.date["weekday"] + \
               "\n" + "temp is between " + \
               self.temp[0] + " and " + self.temp[1] + "degrees\n" + \
               self._wind_info_representation() + " " + "humidity is about " + \
               str(self.humidity) + "\n" + "Generally: " + self.resume

    def prepare_representation(self):
        pass


class FullForecast:
    def __init__(self, weather_record):
        self.date = weather_record["title"]
        self.text_metric = weather_record['fcttext_metric']

    def __str__(self):
        return self.date + "\n" + self.text_metric

    @staticmethod
    def wrap(weather_records):
        all_records = []
        for record in weather_records:
            all_records.append(FullForecast(record))
        return all_records

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
                if self.given_name in city['name'][0:city['name'].index(',')]:
                    return city

            return city_info


def weather_query(city):
    query = QueryAutocomplete(city)
    query_info = query.clarify_query()
    if isinstance(query_info, list) and len(query_info) > 0:
        possible_values = []
        for q in query_info:
            possible_values.append(CityInfo(q['name'], q['c']))
        print("Sorry, your query is not precise, here are the variants, "
              "by autocomplete:")

        for v in possible_values:
            print(v.name, v.c_c)
    elif isinstance(query_info, dict):
        req = CityInfo(query_info['name'][0:query_info['name'].index(',')], query_info['c'])

if __name__ == '__main__':
    parser = get_args_parser()
    # q = QueryResponse()
    # q._raw_weather_response()
    weather_query("Yekaterinburg")
