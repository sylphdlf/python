from flask import Flask
from flask import request
from utils import RedisUtils
import requests

app = Flask(__name__)

redis_ = RedisUtils.get_conn()


@app.route('/getLocation', methods=['GET'])
def getLocation():
    key = redis_.get("amap_key")
    url = "https://restapi.amap.com/v3/ip?ip=%s&output=json&key=%s" % (request.args.get('ip'), key)
    return requests.get(url).json()


if __name__ == '__main__':
    app.run()
