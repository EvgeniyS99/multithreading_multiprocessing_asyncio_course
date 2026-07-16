import socket
from io import BytesIO
from urllib.parse import urlparse


class WSGIRequest:
    def __init__(self, raw_data: bytes):
        self.raw_data = raw_data
        self.method = None
        self.path = None
        self.query_string = ""
        self.server_protocol = "HTTP/1.1"
        self.headers = {}
        self.body = b""

        self._parse()

    def _parse(self):
        header_part, _, body = self.raw_data.partition(b"\r\n\r\n")
        self.body = body

        lines = header_part.decode("utf-8", errors="replace").split("\r\n")
        request_line = lines[0]
        parts = request_line.split()

        if len(parts) != 3:
            raise ValueError("Некорректная строка запроса")

        self.method, raw_target, self.server_protocol = parts

        parsed = urlparse(raw_target)
        self.path = parsed.path
        self.query_string = parsed.query

        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                self.headers[key.upper().replace("-", "_")] = value


class WSGIResponse:
    def __init__(self):
        self.status = "200 OK"
        self.headers = []
        self.body_chunks = []

    def start_response(self, status, headers, exc_info=None):
        self.status = status
        self.headers = headers

    def set_body(self, body_iterable):
        self.body_chunks = list(body_iterable)

    def to_http_bytes(self) -> bytes:
        body = b"".join(
            chunk if isinstance(chunk, bytes) else chunk.encode("utf-8")
            for chunk in self.body_chunks
        )

        headers = dict(self.headers)

        if "Content-Length" not in headers:
            headers["Content-Length"] = str(len(body))
        if "Content-Type" not in headers:
            headers["Content-Type"] = "text/plain; charset=utf-8"

        status_line = f"HTTP/1.1 {self.status}\r\n"
        header_lines = "".join(f"{k}: {v}\r\n" for k, v in headers.items())

        return (status_line + header_lines + "\r\n").encode("utf-8") + body


class WSGIServer:
    def __init__(self, host="127.0.0.1", port=8080, application=None):
        self.host = host
        self.port = port
        self.application = application

    def build_environ(self, request: WSGIRequest):
        environ = {
            "REQUEST_METHOD": request.method,
            "PATH_INFO": request.path,
            "QUERY_STRING": request.query_string,
            "SERVER_NAME": self.host,
            "SERVER_PORT": str(self.port),
            "SERVER_PROTOCOL": request.server_protocol,
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": BytesIO(request.body),
            "wsgi.errors": BytesIO(),   # для учебного примера
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
        }

        for key, value in request.headers.items():
            if key == "CONTENT_TYPE":
                environ["CONTENT_TYPE"] = value
            elif key == "CONTENT_LENGTH":
                environ["CONTENT_LENGTH"] = value
            else:
                environ[f"HTTP_{key}"] = value

        return environ

    def handle_client(self, client_connection):
        raw_data = client_connection.recv(65536)

        try:
            request = WSGIRequest(raw_data)
            environ = self.build_environ(request)

            response = WSGIResponse()
            result = self.application(environ, response.start_response)
            response.set_body(result)

            http_response = response.to_http_bytes()
            client_connection.sendall(http_response)

            if hasattr(result, "close"):
                result.close()

        except Exception as e:
            error_body = f"Internal Server Error\n\n{e}".encode("utf-8")
            http_response = (
                b"HTTP/1.1 500 Internal Server Error\r\n"
                + b"Content-Type: text/plain; charset=utf-8\r\n"
                + f"Content-Length: {len(error_body)}\r\n".encode("utf-8")
                + b"\r\n"
                + error_body
            )
            client_connection.sendall(http_response)

        finally:
            client_connection.close()

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)

            print(f"WSGI server started on http://{self.host}:{self.port}")

            while True:
                client_connection, client_address = server_socket.accept()
                print(f"Connection from {client_address}")
                self.handle_client(client_connection)

class SimpleApp:
    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET")

        if path == "/":
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
            return [b"<h1>Hello from custom WSGI server</h1>"]

        elif path == "/hello":
            start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
            return [f"Hello! Method: {method}".encode("utf-8")]

        else:
            start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
            return [b"Page not found"]
