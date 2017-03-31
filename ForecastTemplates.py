import abc
from utils import wind_directions


class Forecast(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _wind_info_representation(self):
        pass

    @abc.abstractmethod
    def prepare_representation(self):
        pass

    @abc.abstractstaticmethod
    def wrap(self):
        pass


class SimplifiedForecast(Forecast):
    def __init__(self, weather_record):
        print(weather_record)
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
               self.temp[0] + " and " + self.temp[1] + " degrees\n" + \
               self._wind_info_representation() + " " + "humidity is about " + \
               str(self.humidity) + "\n" + "Generally: " + self.resume

    def prepare_representation(self):
        return self.__str__()


class FullForecast(Forecast):

    def _wind_info_representation(self):
        pass

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
