from contextlib import nullcontext
import unittest
import socket
from src.logica.util import HTTPSConnection

class UtilTest(unittest.TestCase):
    def setUp(self):
        self.host ="www.google.com"
        self.port = "80"
        self.timeout = 1
        self.proto = "http"
    
    def testConnection(self):
        self.assertIsNone(HTTPSConnection.connect(self),nullcontext)
    
        