from flask import Flask, jsonify, request, abort
import helper
import json
hostPort = 5001
baseUrl = '/ExchangeServer/api/'
app = Flask(__name__)
client_count = 2
clients = []
n = None
g = None


#Генерация ключей n и g.
#n - простое число
#g - первообразный корень по модулю n
def generate_public_keys():
    global n, g
    n = helper.get_prime(10)
    g = helper.get_rand_prim(n)


#Метод получения общих открытых ключей g и n
@app.route(baseUrl + 'CommonKeys', methods=['GET'])
def get_public_keys():
    global n, g
    if n is None and g is None:
        generate_public_keys()
    return jsonify({'n': n, 'g': g})


#Метод получения активных клиентов
@app.route(baseUrl + 'GetClients', methods=['GET'])
def get_clients():
    global clients
    return json.dumps(clients), 200


#Добавление клиента в список активных клиентов
@app.route(baseUrl + 'RegisterClient', methods=['POST'])
def register_client():
    global clients, client_count
    clients = [x for x in clients if x['url'] != request.json['url']]

    if not request.json or 'url' not in request.json or 'key' not in request.json or len(clients) == client_count:
        abort(400)
    client = {
        'url': request.json['url'],
        'key': request.json['key']
    }
    clients.append(client)
    return get_clients()


#Достаточное количество активных клиентов?
def check_is_ready():
    return len(clients) == client_count


#Проверяем, нужно ли ждать еще клиентов
@app.route(baseUrl + 'IsReadyForExchange', methods=['GET'])
def is_ready_for_exchange():
    global clients, client_count
    return jsonify({'Status': check_is_ready()}), 200


#Отдаем список - клиент + его открытый ключ
@app.route(baseUrl + 'GetClientsPublicKeys', methods=['GET'])
def get_clients_public_keys():
    if check_is_ready():
        return jsonify({clients}), 200
    else:
        abort(400)


if __name__ == '__main__':
    generate_public_keys()
    app.run(debug=True, port=hostPort)
