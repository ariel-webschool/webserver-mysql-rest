from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from models.Users import Users

class UserHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        usersHandler = Users()
        if self.path == '/users':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            users = usersHandler.all()
            self.wfile.write(json.dumps({'users': users}).encode('utf-8'))
        elif self.path.startswith('/users/'):
            try:
                user_id = int(self.path.split('/')[-1])
                user = usersHandler.find(user_id)
                if user is None:
                    self.send_response(404)
                    self.wfile.write(json.dumps({'error': 'User not found'}).encode('utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'user': user}).encode('utf-8'))
            except ValueError:
                self.send_response(400)
                self.wfile.write(json.dumps({'error': 'Invalid ID'}).encode('utf-8'))

    def do_POST(self):
        userHandler = Users()
        if self.path == '/users':
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                post_data = json.loads(post_data)
                user_added = userHandler.add(post_data)
                print(user_added)
                if user_added:
                    self.send_response(201)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'user': post_data}).encode('utf-8'))
                else:
                    raise Error("Error overcome due by user added.")
            except (json.JSONDecodeError, KeyError):
                self.send_response(400)
                self.wfile.write(json.dumps({'error': 'Bad request'}).encode('utf-8'))

    def do_PUT(self):
        usersHandler = Users()
        if self.path.startswith('/users/'):
            try:
                id = int(self.path.split('/')[-1])
                user_exist = usersHandler.find(id)
                if user_exist is None:
                    self.send_response(404)
                    self.wfile.write(json.dumps({'error': 'User not found'}).encode('utf-8'))
                    return
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(put_data)
                user_updated = usersHandler.update(id,data)
                if user_updated:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'user': data, 'message': "User Updated!"}).encode('utf-8'))
            except (ValueError, json.JSONDecodeError):
                self.send_response(400)
                self.wfile.write(json.dumps({'error': 'Bad request'}).encode('utf-8'))

    def do_DELETE(self):
        usersHandler = Users()
        if self.path.startswith('/users/'):
            try:
                user_id = int(self.path.split('/')[-1])
                user_exist = usersHandler.find(user_id)
                if user_exist is None:
                    self.send_response(404)
                    self.wfile.write(json.dumps({'error': 'User not found'}).encode('utf-8'))
                    return
                user_removed = usersHandler.delete(user_id)
                if user_removed:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps({'result': True}).encode('utf-8'))
                else:
                    raise Error("User not exist")
            except ValueError:
                self.send_response(400)
                self.wfile.write(json.dumps({'error': 'Invalid ID'}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=UserHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
