import socket
import threading
import game
def doska(board):
    s = ''
    for i in range(0,8):
        for j in range(8):
            s += board[i][j]
        s += '\n'
    return s
server = socket.socket()

server.bind(("", 9091))

server.listen(5)
users = []
users_A=[]
print("Server is listening")
board = [['/', '/', '/', '/','/', '/', '/', '/'],['L', '/', '/', '/','/', '/', '/', '/'],
         ['/', '/', '/', '/','K', '/', '/', '/'],['/', '/', '/', '/','/', '/', '/', '/'],
         ['/', '/', '/', '/','/', '/', '/', '/'],['/', '/', '/', '/','/', '/', '/', '/'],
         ['/', '/', '/', '/','/', '/', '/', '/'],['/', '/', '/', '/','/', '/', '/', 'L']]


def send_all(data):
    for user in users:
        # user.send(data)
        user.send(bytes(data, encoding="UTF-8"))

turn = 0
def listen_user(user, name):
    global turn
    print('Listening user')
    while True:
        data = user.recv(1024)
        data = data.decode(encoding='UTF-8')
        print(data)
        if name == users_A[0] and game.turn_move % 2 == 0:
            message = game.move(data,board)
        elif name == users_A[1] and game.turn_move % 2 == 1:
            message = game.hozhu(data,board)
        elif name == users_A[0] and game.turn_move % 2 == 1:
            message = 'Не ваш ход'
        elif name == users_A[1] and game.turn_move % 2 == 0:
            message = 'Не ваш ход'
        else:
            continue
        send_all(message)
        if message == 'Ахахаххахахахах лаьди выиграли':
            break


def start_server():
    while True:
        user_socket, address = server.accept()
        print(f"User <{address[1]}> connected")
        users.append(user_socket)
        users_A.append(address[1])
        listen_accepted_user = threading.Thread(
            target=listen_user,
            args=(user_socket, address[1])
            )
        user_socket.send(doska(board).encode('utf-8'))
        if len(users) == 1:
            user_socket.send("Вы играете за ладью".encode('utf-8'))
        elif len(users) == 2:
            user_socket.send("Вы играете за короля".encode('utf-8'))
        else:
            user_socket.send("Вы просто зритель".encode('utf-8'))
        listen_accepted_user.start()
if __name__ == '__main__':
    start_server()
