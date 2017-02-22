from api import coin
import json
from flask import Flask, request, jsonify, Markup, render_template
app = Flask(__name__)


coin = coin.Coin()


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/checkout")
def checkout():
    metadata = {
        'Name': 'Joe Doe',
        'Email address':'joe.doe@example.com',
        'Shipping address': '123 5th Avenue',
        'City': 'Portland',
        'State': 'OR',
        'Postal Code': '97171',
    }
    source = coin.create_source(amount_in_cents=123, metadata=metadata, email='joe.doe@example.com')
    data = dict()
    data['source_id'] = source.id
    data['uri'] = source.bitcoin.uri
    data['amount'] = source.amount
    img_uri = coin.generate_qrcode(source.bitcoin.uri)
    print(json.dumps(data))
    img = Markup('<img src="data:image/png;base64,' + img_uri + '" />')
    return render_template('checkout.html', img=img, data=json.dumps(data))

@app.route("/notifications", methods=['POST'])
def notifications():
    payload = request.json
    payload_type = payload['type']
    print('New notification: ' + payload_type)
    if payload_type == 'source.chargeable':
        source = payload['data']['object']
        source_id = source['id']
        charge = coin.create_charge(
            amount=source['amount'],
            currency=source['currency'],
            source_id=source_id,
            receipt_email=source['owner']['email'],
            description=source['owner']['email'],
            metadata=source['metadata'])
        print('source id: ' + source_id)
        print('charge id: ' + charge.id)
    elif payload_type == 'charge.succeeded':
        charge = payload['data']['object']
        source = charge['source']
        charge_id = charge['id']
        source_id = source['id']
        print('source id: ' + source_id)
        print('charge id: ' + charge_id)
    elif payload_type == 'source.canceled':
        source = payload['data']['object']
        source_id = source['id']
        print('source id: ' + source_id)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


if __name__ == "__main__":
    app.run()
