import json
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/notifications", methods=['POST'])
def paid():
    payload = request.json
    # print(json.dumps(payload))
    payload_type = payload['type']
    print('payload type: ' + payload_type)
    if payload_type == 'source.chargeable':
        source = payload['data']['object']
        source_id = source['id']
        print('source id: ' + source_id)
    elif payload_type == 'charge.succeeded':
        payment = payload['data']['object']
        payment_id = payment['id']
        print('payment id: ' + payment_id)
    return jsonify(request.json)

@app.route("/orders/<order_id>/receipt")
def receipt(order_id):
    return str(order_id)

if __name__ == "__main__":
    app.run()