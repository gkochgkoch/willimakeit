from datetime import datetime

from pydantic import BaseModel


class WeatherProviderError(Exception):
    pass


class WeatherProviderNoContentError(WeatherProviderError):
    pass


class WeatherProvider503Error(WeatherProviderError):
    pass


class WeatherProviderTimeoutError(WeatherProviderError):
    pass


class HourlyWeather(BaseModel):
    timestamp: datetime
    visibility: float
    snowfall: float
    wind_speed_80m: float


class Weather(BaseModel):
    hourly: list[HourlyWeather]
