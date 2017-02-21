import json
from flask import Flask, request, jsonify
app = Flask(__name__)


class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/notifications", methods=['POST'])
def paid():
    payload = Payload(request.json)
    print('New notification: ' + payload.type)
    if payload.type == 'source.chargeable':
        source = payload.data.object
        print('source id: ' + source.id)
    elif payload.type == 'source.canceled':
        source = payload['data']['object']
        source_id = source['id']
        print('source id: ' + source_id)
        print(json.dumps(source))
    elif payload.type == 'charge.succeeded':
        charge = payload.data.object
        source = charge.source
        print('source id: ' + source.id)
        print('charge id: ' + charge.id)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


if __name__ == "__main__":
    app.run()
