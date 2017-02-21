import coin
import json
from flask import Flask, request, jsonify
app = Flask(__name__)


coin = Coin()


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/checkout", methods=['POST'])
def checkout():
    source = coin.create_source()
    print('source id: ' + source.id)
    coin.generate_qrcode(source.bitcoin.uri)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/notifications", methods=['POST'])
def notifications():
    payload = request.json
    payload_type = payload['type']
    print('New notification: ' + payload_type)
    if payload_type == 'source.chargeable':
        source = payload['data']['object']
        source_id = source['id']
        print('source id: ' + source_id)
        # This method should be called in the callback,
        # source is retrieved from source.chargeable event payload
        charge = coin.create_charge(
            amount=source['amount'],
            currency=source['currency'],
            source=source_id,
            receipt_email=source['owner']['email'],
            description=source['owner']['email'],
            metadata=source['metadata'])
        print(charge)
    elif payload_type == 'source.canceled':
        source = payload['data']['object']
        source_id = source['id']
        print('source id: ' + source_id)
    elif payload_type == 'charge.succeeded':
        charge = payload['data']['object']
        source = charge['source']
        charge_id = charge['id']
        source_id = source['id']
        print('source id: ' + source_id)
        print('charge id: ' + charge_id)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


if __name__ == "__main__":
    app.run()
