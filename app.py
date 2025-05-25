import ssl
import os
from subprocess import run

import http.server

PORT = 4443
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path in ('/', '/index.htm', '/index.html'):
            self.path = '/index.htm'
        return super().do_GET()

if __name__ == "__main__":
    httpd = http.server.HTTPServer(('0.0.0.0', PORT), Handler)

    # Generate a self-signed certificate if not present
    cert_file = os.path.join(DIRECTORY, 'cert.pem')
    key_file = os.path.join(DIRECTORY, 'key.pem')
    if not (os.path.exists(cert_file) and os.path.exists(key_file)):
        print("Generating self-signed certificate...")
        run([
            'C:\\Program Files\\OpenSSL-Win64\\bin\\openssl', 'req', '-new', '-x509', '-days', '365',
            '-nodes', '-out', cert_file, '-keyout', key_file,
            '-subj', '/CN=localhost'
        ], check=True)

    # Use SSLContext instead of deprecated ssl.wrap_socket
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Serving HTTPS on https://localhost:{PORT}/")
    httpd.serve_forever()