import requests
from winotify import Notification as WinNotification
from requests.exceptions import RequestException
from json.decoder import JSONDecodeError

CITY = "Лиссабон"
API_KEY = "23496c2a58b99648af590ee8a29c5348"
UNITS = "metric"
LANGUAGE = "ru"


class WeatherRequestError(Exception):
    pass


class WeatherRequst:
    def __init__(self, api_key: str, units: str = "metric", language: str = "ru"):
        self.api_key = api_key
        self.units = units
        self.language = language
        self.__url: str = ""
        self.__response: dict = {}

    def __get_request_url(self, city: str):
        self.__url = rf"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units={self.units}&lang={self.language}"

    def get_weather(self, city: str):
        try:
            self.__get_request_url(city)
            response = requests.get(self.__url, timeout=5)
            response.raise_for_status()
            self.__response = response.json()
        except RequestException as e:
            raise WeatherRequestError(f"Ошибка при запросе погоды: {str(e)}")
        except JSONDecodeError:
            raise WeatherRequestError("Получен некорректный ответ от сервера")

    def get_clear_weather_data(self, city: str):
        self.get_weather(city)
        result_dict = {}
        result_dict["temp"] = self.__response["main"]["temp"]
        result_dict["feels_like"] = self.__response["main"]["feels_like"]
        result_dict["description"] = self.__response["weather"][0]["description"]
        return result_dict

    def get_weather_string(self, weather_dict: dict) -> str:
        temp = weather_dict["temp"]
        feels_like = weather_dict["feels_like"]
        description = weather_dict["description"]
        return f"Температура: {temp}°C\nОщущается как: {feels_like}°C\nОписание: {description}"

    def __call__(self, city: str) -> str:
        weather_dict = self.get_clear_weather_data(city)
        return self.get_weather_string(weather_dict)

