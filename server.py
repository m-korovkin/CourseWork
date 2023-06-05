import socket
import sys
import datetime

from models import Request, Response
import wsgi, config


class HTTPServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        # self.blacklist = []

    def run_server(self):
        print(f'[{datetime.datetime.now()}] [OK] "Server is running..."')
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip, self.port))
            backlog = 10  # Размер очереди входящих подключений, т.н. backlog
            server_socket.listen(backlog)

            while True:
                client_socket, address = server_socket.accept()
                self.serve_client(client_socket)
        except KeyboardInterrupt as exit:
            server_socket.close()
            print(f"[{datetime.datetime.now()}] [!] Server successfully closed. Bye!")

    def serve_client(self, client_socket):
        data = client_socket.recv(1024).decode('utf-8')
        try:
            var = data[0]
            #print(data)
            request = self.parse_request(data)
            response_data = self.handle_request(request)
            response = f'HTTP/1.1 {response_data.status} {response_data.reason}\r\n'
            if response_data.headers:
                for (key, value) in response_data.headers:
                    response += f'{key}: {value}\r\n'
            response += '\r\n'
            #print(response)
            response = response.encode('utf-8')
            if response_data.body:
                response = response + response_data.body
            client_socket.send(response)
            client_socket.shutdown(socket.SHUT_WR)
        except IndexError as e:
            print(f'[{datetime.datetime.now()}] [ERROR] [{e}]')
            client_socket.shutdown(socket.SHUT_WR)

        

    def parse_request(self, data):
        query, body = None, None
        data_array = data.split()
        method, target, version = data_array[0], data_array[1], data_array[2]
        if str(target).find('?') != -1:
            query = target[str(target).find('?')+1:]
            target = target[:str(target).find('?')]
        if target == '/': target = f'/{config.mainPageName}'
        headers_array = data_array[3:]        
        for element in data_array:
            if 'Content-Length' in str(element):
                body = headers_array.pop(-1)
                print(f'[{datetime.datetime.now()}] "{method} {target} {version} {query} {body}"')
                return Request(method, target, version, headers_array, body=body)
        else:
            print(f'[{datetime.datetime.now()}] "{method} {target} {version} {query} {body}"')
            return Request(method, target, version, headers_array, query=query)

 
    def handle_request(self, request):
        try:
            path = request.target
            content_type, body, status, reason = '', '', '', ''

            if 'GET' in str(request.method) and 'getTicketsList' in str(path):
                return wsgi.handleGetTickets(request)
            elif 'GET' in str(request.method) and '/index.html' in str(path):
                return wsgi.handleGetAllTickets(request)
            elif 'GET' in str(request.method) and '/tickets.html' in str(path):
                return wsgi.handleGetAllTicketsAdmin(request)
            elif 'POST' in str(request.method) and 'createTicket' in str(path):
                return wsgi.handleCreateTicket(request)
            elif 'POST' in str(request.method) and 'buyTicket' in str(path):
                return wsgi.afterShowTicket(request)
            elif 'POST' in str(request.method) and 'backToMain' in str(path):
                return wsgi.handleBuyTicket(request)
            elif ('POST' in str(request.method) and 'choosePlace' in str(path)):
                return wsgi.handleGetAllPlaces(request)
            elif 'POST' in str(request.method) and 'passportData' in str(path):
                return wsgi.handleGetPassportData(request)
            elif ('POST' in str(request.method) and 'enterAdminPanel' in str(path)):
                return wsgi.handleLoginAdmin(request)
            elif 'POST' in str(request.method) and 'returnTicket' in str(path):
                return wsgi.handleReturnTicket(request)
            elif '.html' in str(path):
                content_type = 'text/html; charset=uft-8'
            elif '.css' in str(path):
                content_type = 'text/css'
            else:
                 pass # TODO сообщение об ошибке

            with open(f'{config.directoryName}{path}', 'rb') as file:
                body = file.read()
            status, reason = '200', 'OK'
            headers = [('Content-Type', content_type), ('Content-Length', len(body))]
        except Exception as err:
            print(f'[{datetime.datetime.now()}] [ERROR] [{err}]')
            body = 'Sorry, bro! No page...'.encode('utf-8')
            content_type = 'text/html; charset=uft-8'
            status, reason = '404', 'Not Found'
            headers = [('Content-Type', content_type), ('Content-Length', len(body))]
        return Response(status, reason, headers, body)


if __name__ == '__main__':
    # host = sys.argv[1] # ip address
    host = '127.0.0.1'
    # port = int(sys.argv[2])
    port = 53210
    
    serv = HTTPServer(host, port)
    serv.run_server()
