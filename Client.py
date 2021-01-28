import threading
import socket
import argparse
import os


class Send(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        while True:
            message = input('{}: '.format(self.name))

            # Type 'QUIT' to leave the chatroom
            if message == 'QUIT':
                self.sock.sendall('Server: {} đã rời khỏi cuộc trò chuyện.'.format(
                    self.name).encode('utf-8'))
                break

            # Send message to server for broadcasting
            else:
                self.sock.sendall('{}: {}'.format(
                    self.name, message).encode('utf-8'))

        print('\nĐang thoát...')
        self.sock.close()
        os._exit(0)


class Receive(threading.Thread):

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):

        while True:
            message = self.sock.recv(1024)
            if message:
                print('\r{}\n{}: '.format(
                    message.decode('utf-8'), self.name), end='')
            else:
                # Server has closed the socket, exit the program
                print('\nMất kết nối')
                print('\nĐang thoát')
                self.sock.close()
                os._exit(0)


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        print('Đang kết nối tới {}:{}...'.format(self.host, self.port))
        self.sock.connect((self.host, self.port))
        print('Kết nối thành công đến {}:{}'.format(self.host, self.port))

        print()
        name = input('Nhập biệt danh: ')

        print()
        print('Sẳn sàn gửi và nhận tin nhắn')

        # Create send and receive threads
        send = Send(self.sock, name)
        receive = Receive(self.sock, name)

        # Start send and receive threads
        send.start()
        receive.start()

        self.sock.sendall(
            'Server: {} đã tham gia vào cuộc trò chuyện'.format(name).encode('utf-8'))
        print("\rGõ 'QUIT' nếu muốn thoát\n")
        print('{}: '.format(name), end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()

    client = Client(args.host, args.p)
    client.start()
