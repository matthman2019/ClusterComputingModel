from Client import Client
import pathlib
from ctypes import cdll, c_char_p, c_bool

import sys

if sys.platform.startswith('win'):
    mersenne_library = cdll.LoadLibrary(pathlib.Path(__file__).parent / "mersenne.dll")
elif sys.platform.startswith('linux'):
    print("This program is running on Linux.")
    mersenne_library = cdll.LoadLibrary(pathlib.Path(__file__).parent / "mersenne.so")

mersenne_library.is_mersenne_prime.argtypes = [c_char_p]
mersenne_library.is_mersenne_prime.restype = c_bool


N = "N".encode()

IP = "192.168.0.37"
PORT = 15555

def is_mersenne_prime(number : str):
    number = int(number)
    mersenne_number = (2 ** number) - 1
    s = 4
    for i in range(number - 2):
        s = ((s * s) - 2) % mersenne_number
    return s == 0

if __name__ == "__main__":
    
    client = Client((IP, PORT), lambda numberString: mersenne_library.is_mersenne_prime(str(numberString).encode()), 8, False, True)
    client.start()
