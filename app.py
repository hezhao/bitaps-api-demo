import json
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/notifications", methods=['POST'])
def paid():
    print(json.dumps(request.json))
    print(request.json.type)
    notification = request.json.data
    print(notification.status, notification.transaction.id)
    return jsonify(request.args)

@app.route("/orders/<order_id>/receipt")
def receipt(order_id):
    return str(order_id)

if __name__ == "__main__":
    app.run()