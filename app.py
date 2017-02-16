import json
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/paid", methods=['POST'])
def paid():
    print(str(request))
    print(dir(request))
    print(json.dumps(request.form))
    print(json.dump(request.args))
    return jsonify(request.args)


if __name__ == "__main__":
    app.run()
