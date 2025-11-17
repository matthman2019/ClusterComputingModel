from Client import Client
import pathlib
from ctypes import cdll, c_char_p, c_bool

import sys

if sys.platform.startswith('win'):
    mersenne_library = cdll.LoadLibrary(pathlib.Path(__file__).parent / "mersenne.dll")
elif sys.platform.startswith('linux'):
    mersenne_library = cdll.LoadLibrary(pathlib.Path(__file__).parent / "mersenne.so")

mersenne_library.is_mersenne_prime.argtypes = [c_char_p]
mersenne_library.is_mersenne_prime.restype = c_bool


N = "N".encode()

IP = "127.0.0.1"
PORT = 15555

def is_mersenne_prime(number : str):
    number = int(number)
    mersenne_number = (2 ** number) - 1
    s = 4
    for i in range(number - 2):
        s = ((s * s) - 2) % mersenne_number
    return s == 0

def mersenne_library(number : str):
    return mersenne_library.is_mersenne_prime(number.encode())

if __name__ == "__main__":
    
    client = Client((IP, PORT), mersenne_library, 8, False, True)
    client.start()
