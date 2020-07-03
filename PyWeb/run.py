from flask import Flask
from flask import request
from PyWeb.utils import RedisUtils
import requests
import json

app = Flask(__name__)

redis_ = RedisUtils.get_conn()


@app.route('/cityAndWeather', methods=['GET'])
def getLocation():
    key = redis_.get("amap_key")
    location_last_url = "https://restapi.amap.com/v3/ip?ip=%s&output=json&key=%s" % (request.args.get('lastIp'), key)
    location_now_url = "https://restapi.amap.com/v3/ip?ip=%s&output=json&key=%s" % (request.args.get('ip'), key)
    location_last = requests.get(location_last_url).json()
    location_now = requests.get(location_now_url).json()
    last_city = location_last['city']
    city_code = location_now['adcode']
    weather_url_live = "https://restapi.amap.com/v3/weather/weatherInfo?city=%s&extensions=base&key=%s" % (city_code, key)
    weather_url_forecast = "https://restapi.amap.com/v3/weather/weatherInfo?city=%s&extensions=all&key=%s" % (city_code, key)
    weather_live = requests.get(weather_url_live).json()
    weather_forecast = requests.get(weather_url_forecast).json()
    result = json.dumps({"city": last_city, "lives": weather_live['lives'], "forecasts": weather_forecast['forecasts']})
    return result


if __name__ == '__main__':
    app.run()
