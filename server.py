import socket
import sys

from messages import Request, Response
import wsgi, config


class HTTPServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        # self.blacklist = []

    def run_server(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip, self.port))
            backlog = 10  # Размер очереди входящих подключений, т.н. backlog
            server_socket.listen(backlog)

            while True:
                client_socket, address = server_socket.accept()
                self.serve_client(client_socket)
        except KeyboardInterrupt:
            server_socket.close()

    def serve_client(self, client_socket):
        data = client_socket.recv(1024).decode('utf-8')
        print(data)
        request = self.parse_request(data)
        response_data = self.handle_request(request)
        response = f'HTTP/1.1 {response_data.status} {response_data.reason}\r\n'
        if response_data.headers:
            for (key, value) in response_data.headers:
                response += f'{key}: {value}\r\n'
        response += '\r\n'
        print(response)
        response = response.encode('utf-8')
        if response_data.body:
            response = response + response_data.body
        client_socket.send(response)
        client_socket.shutdown(socket.SHUT_WR)

    def parse_request(self, data):
        query, body = None, None
        data_array = data.split()
        print(data_array)
        method, target, version = data_array[0], data_array[1], data_array[2]
        if str(target).find('?') != -1:
            query = target[str(target).find('?')+1:]
            target = target[:str(target).find('?')]
        if target == '/': target = f'/{config.mainPageName}'
        headers_array = data_array[3:]        
        for element in data_array:
            if 'Content-Length' in str(element):
                body = headers_array.pop(-1)
                return Request(method, target, version, headers_array, body=body)
        else:
            return Request(method, target, version, headers_array, query=query)
 
    def handle_request(self, request):
        path = request.target
        content_type, body, status, reason = '', '', '', ''

        if 'GET' in str(request.method) and 'getTicketsList' in str(path):
            return wsgi.handleGetTickets(request)
        elif 'POST' in str(request.method) and 'buyTicket' in str(path):
            return wsgi.handleBuyTicket(request)
        elif 'POST' in str(request.method) and 'returnTicket' in str(path):
            return wsgi.handleReturnTicket(request)
        elif '.html' in str(path):
            content_type = 'text/html; charset=uft-8'
        elif '.css' in str(path):
            content_type = 'text/css'
        else:
            pass # TODO сообщение об ошибке

        """
        elif 'POST' in str(request.method):
            print('POST wsgi.py')
            return wsgi.handle_create_user(request)
        elif 'wsgi.py' in str(path) and 'GET' in str(request.method):
            print('GET wsgi.py')
            return wsgi.handle_get_users(request)
        elif 'page.html' in str(path):
            return wsgi.handle_get_tasks(request)
        """

        try:
            with open(f'{config.directoryName}{path}', 'rb') as file:
                body = file.read()
            status, reason = '200', 'OK'
        except:
            body = 'Sorry, bro! No page...'.encode('utf-8')
            status, reason = '404', 'Not Found'
        headers = [('Content-Type', content_type), ('Content-Length', len(body))]
        return Response(status, reason, headers, body)


if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    serv = HTTPServer(host, port)
    serv.run_server()