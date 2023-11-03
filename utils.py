import os
import socket
import gmpy2
import sympy
import hashlib
from random import randint

LOCAL_PORT = 4080
SERVER_HOST = "127.0.0.1"

L = 256

def pack(s, splitter=b'-'):
    res = b''
    for x in s:
        res += n2b(x)+splitter
    if(res==b''):
        return res
    return res[:-1]

def hash(t):
    h = hashlib.new('sha512_256')
    h.update(t)
    return h.hexdigest().encode('utf8')

def n2b(n):
    return str(n).encode("utf8")

def nbit_prime(l = L):
    bstr = os.urandom(1//8)
    rnum = int.from_bytes(bstr, "big")
    return gmpy2.next_prime(rnum)

class CyclicGroup:
    def __init__(self, p=None, g=None):
        self.p = p or nbit_prime()
        self.generator = g or self.find_generator()
    def pow(self, base, exponent):
        return pow(base, exponent, self.p)
    def mul(self, num1, num2):
        return (num1 * num2) % self.p
    def div(self, a, b):
        return self.mul(a, pow(b, self.p-2, self.p))
    def rand_int(self):
        return randint(1, self.p-1)
    def find_generator(self):
        factors = sympy.primefactors(self.p-1)
        while True:
            candidate = self.rand_int()
            for factor in factors:
                if 1 == self.pow(candidate, (self.p -1) // factor):
                    break
            else:
                return candidate

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, LOCAL_PORT))
    return s

def listen():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((SERVER_HOST, LOCAL_PORT))
    serversocket.listen(5)
    return serversocket