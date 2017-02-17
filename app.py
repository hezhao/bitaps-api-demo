import json
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/notifications", methods=['POST'])
def paid():
    payload = request.json
    print(json.dumps(payload))
    source = payload['data']['object']['source']
    print('payload type: ' + payload['type'])
    print('source id: ' + source['id'])
    return jsonify(request.json)

@app.route("/orders/<order_id>/receipt")
def receipt(order_id):
    return str(order_id)

if __name__ == "__main__":
    app.run()