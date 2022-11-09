import socket
import ssl

class HTTPSConnection():

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if not hasattr(ssl, 'SSLContext'):
            if self.ca_certs:
                cert_reqs = ssl.CERT_REQUIRED
            else:
                cert_reqs = ssl.CERT_NONE
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                                        cert_reqs=cert_reqs,
                                        ssl_version=ssl.PROTOCOL_TLSv1_2,
                                        ca_certs=self.ca_certs)  
        sock.close()


