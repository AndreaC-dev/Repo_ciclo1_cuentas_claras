
import logging
import re
import socket
try:
    import ssl
except ImportError:  # pragma: no cover
    ssl = None


logger = logging.getLogger(__name__)

IDENTIFIER = re.compile(r'^([\w\.-]+)\s*')
VERSION_IDENTIFIER = re.compile(r'^([\w\.*+-]+)\s*')
COMPARE_OP = re.compile(r'^(<=?|>=?|={2,3}|[~!]=)\s*')
MARKER_OP = re.compile(r'^((<=?)|(>=?)|={2,3}|[~!]=|in|not\s+in)\s*')
OR = re.compile(r'^or\b\s*')
AND = re.compile(r'^and\b\s*')
NON_SPACE = re.compile(r'(\S+)\s*')
STRING_CHUNK = re.compile(r'([\s\w\.{}()*+#:;,/?!~`@$%^&=|<>\[\]-]+)')

class HTTPSConnection(httplib.HTTPSConnection):

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if not hasattr(ssl, 'SSLContext'):
            # For 2.x
            if self.ca_certs:
                cert_reqs = ssl.CERT_REQUIRED
            else:
                cert_reqs = ssl.CERT_NONE
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                                        cert_reqs=cert_reqs,
                                        ssl_version=ssl.PROTOCOL_TLSv1_2,
                                        ca_certs=self.ca_certs)


