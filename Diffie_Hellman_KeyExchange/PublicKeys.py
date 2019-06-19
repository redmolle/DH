from flask import Flask, jsonify, request, abort

baseUrl = '/PublicKeys/api/'
public_keys = [
    {
        'n': 0,
        'g': 0
    }
]
app = Flask(__name__)


@app.route(baseUrl + 'GetKeys', methods=['GET'])
def get_keys():
    return jsonify({'PublicKeys': public_keys}), 200


if __name__ == '__main__':
    app.run(Debug=True)
