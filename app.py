from urllib.request import urlopen


import json
import os


from flask import Flask
from flask import request
from flask import make_response


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = fulfillRequest(req)

    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def fulfillRequest(req):
    if req.get("result").get("action") != "getExchangeRate":
        return {}

    baseUrl = "https://api.cryptonator.com/api/ticker/"

    currencies = getCurrencies(req)
    if len(currencies) != 2:
        return {}
    reqUrl = baseUrl + "-".join(currencies)

    result = urlopen(reqUrl).read()
    data = json.loads(result)
    res = formatWebhook(data)
    return res


def getCurrencies(req):
    result = req.get("result")
    params = result.get("parameters")

    currencies = []
    base = params.get("currency-base")
    if base is not None:
        currencies.append(base)
    target = params.get("currency-target")
    if target is not None:
        currencies.append(target)
    return currencies


def formatWebhook(data):
    requestSuccess = data.get("success")
    if not requestSuccess:
        return {}

    ticker = data.get("ticker")

    base = ticker.get("base")
    target = ticker.get("target")
    price = ticker.get("price")
    change = ticker.get("change")
    timestamp = data.get("timestamp")

    if base is None or target is None or price is None or \
            change is None or timestamp is None:
        return {}

    speech = "1 " + base + " is trading for " + price \
        + " " + target

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": data,
        "contextOut": [],
        "source": "crypto-exchange-rate"
    }


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port " + str(port))

    app.run(debug=True, port=port, host='0.0.0.0')
