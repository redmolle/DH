import requests as req
import helper
import json

hostPort = 5001
baseUrl = 'Alice/api/'
serverUrl = 'http://127.0.0.1:5001/ExchangeServer/api/'
a = None
A = None
n = None
g = None
K = None
clients = []


#Получаем с сервиса n и g
def get_common_keys():
    res = req.get(serverUrl + 'CommonKeys')
    if res.status_code == 200:
        global n, g
        n = res.json()['n']
        g = res.json()['g']

        msg = 'Common keys accepted'
    else:
        msg = 'Error in get_common_keys()'
    print(msg)


#Регистрируем клиента вместе с его открытым ключом
def register():
    if n is None or g is None:
        print('Need to DownloadCommonKeys')
        return
    global a, A
    a = helper.get_prime(1024)
    A = helper.mod(g, a, n)
    res = req.post(serverUrl + 'RegisterClient', json={'url': baseUrl, 'key': A})
    if res.status_code == 201 or res.status_code == 200:
        msg = 'Client were added to conversation'
    elif res.status_code == 412:
        msg = 'Conversation already full'
    else:
        msg = 'Error on register()'
    print(msg)


#Проверяем готовность сервера
def check_server_is_ready():
    res = req.get(serverUrl + 'IsReadyForExchange')
    if res.status_code == 200 and 'Status' in res.json():
        global isReadyServer
        if res.json()['Status']:
            msg = 'Server ready'
            isReadyServer = True
        else:
            msg = 'Server not ready'
            isReadyServer = False
    else:
        msg = 'Error on check_server_is_ready()'
        isReadyServer = False
    print(msg)


#Получаем список - клиент + его открытый ключ
def get_client_keys():
    if n is None or g is None or a is None or A is None:
        print('Need to DownloadCommonKeys')
        return
    res = req.get(serverUrl + 'GetClientsPublicKeys')
    if res.status_code == 200:
        msg = 'Clients accepted'
        global clients
        clients = res.json()
        set_private_key()
    else:
        msg = 'Error on get_clients_keys()'
    print(msg)


#Считаем закрытый ключ
def set_private_key():
    if n is None or g is None or a is None or A is None:
        print('Need to DownloadCommonKeys')
        return
    elif len(clients) == 0:
        print('Need to DownloadClientPublicKeys')
        return
    global K
    _exp = [x for x in clients if x['url'] != baseUrl]
    exp = 1
    for i in range(len(_exp)):
        exp = exp * _exp[i]['key']

    K = helper.mod(exp, a, n)


def print_keys():
    data = [
        {'PublicKeys': {
            'n': n,
            'g': g,
            'A': A
        }},
        {'PrivateKeys': {
            'K': K,
            'a': a
        }}
    ]

    print(json.dumps(data))


def switch_command():
    print('\n\n0.Exit')
    print('1.DownloadCommonKeys')
    print('2.Register')
    print('3.CheckServerIsReady')
    print('4.DownloadClientPublicKeys')
    print('5.PrintKeys')
    answer = input('Answer >> ')

    while True:
        if answer == '0':
            return False
        elif answer == '1':
            get_common_keys()
            break
        elif answer == '2':
            register()
            break
        elif answer == '3':
            check_server_is_ready()
            break
        elif answer == '4':
            get_client_keys()
            break
        elif answer == '5':
            print_keys()
            break
        else:
            answer = input('Enter correct answer >> ')
            print()
    return True


if __name__ == '__main__':
    cmd = switch_command()
    while cmd:
        cmd = switch_command()

