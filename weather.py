import xml.etree.ElementTree as ET
import requests
from speak import speak
from robot_keys import app_id


def get_temp(forecast, fahrenheit=True):
    """
    Return temp from a specified forecast

    Parameters
    ----------
    forecast : object
        XML forecast object
    fahrenheit : bool, optional (default = True)
        Whether to return temp in fahrenheit or celsius

    Returns
    -------
    temperature : float

    """
    precipitation_idx = [child.tag for child in forecast].index('temperature')
    precipitation = forecast[precipitation_idx]
    if fahrenheit:
        multiplier =  9/5.
        offset = 32.
    else:
        multiplier = 1.
        offset = 0

    return float(precipitation.attrib['value']) * multiplier + offset # convert to Fahrenheit

def get_precipitation(forecast):
    """
    Return inches of precipitation from a specified forecast

    Parameters
    ----------
    forecast : object
        XML forecast object

    Returns
    -------
    precipitation : float
        precipitation measured in inches
    """
    precipitation_idx = [child.tag for child in forecast].index('precipitation')
    precipitation = forecast[precipitation_idx]
    if len(precipitation.attrib) > 0:
        return float(precipitation.attrib['value']) * 0.03937007874  # convert to inches
    else:
        return 0


def get_weather(forecast_id=0):
    data = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?q=wareham,us&mode=xml&appid='+app_id
    )

    root = ET.fromstring(data.text)
    forecast_idx = [child.tag for child in root].index('forecast')
    forecast = root[forecast_idx][forecast_id]

    precip = get_precipitation(forecast)
    if precip == 0:
        speak("No rain in the next 3 hours.  Hooray!")
    else:
        speak("{0} inches of precipitation forecasted in the next 3 hours".format(round(precip, 2)))

    temp = get_temp(forecast)
    speak("Temperature is expected to be {0}".format(round(temp, 1)))

if __name__ == '__main__':

    get_weather()