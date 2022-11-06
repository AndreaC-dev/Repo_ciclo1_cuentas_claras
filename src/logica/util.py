#
# Copyright (C) 2012-2017 The Python Software Foundation.
# See LICENSE.txt and CONTRIBUTORS.txt.
#
import codecs
from collections import deque
import contextlib
import csv
from glob import iglob as std_iglob
import io
import json
import logging
import os
import py_compile
import re
import socket
try:
    import ssl
except ImportError:  # pragma: no cover
    ssl = None
import subprocess
import sys
import tarfile
import tempfile
import textwrap

try:
    import threading
except ImportError:  # pragma: no cover
    import dummy_threading as threading
import time

from . import DistlibException
from .compat import (string_types, text_type, shutil, raw_input, StringIO,
                     cache_from_source, urlopen, urljoin, httplib, xmlrpclib,
                     splittype, HTTPHandler, BaseConfigurator, valid_ident,
                     Container, configparser, URLError, ZipFile, fsdecode,
                     unquote, urlparse)

logger = logging.getLogger(__name__)

#
# Requirement parsing code as per PEP 508
#

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


