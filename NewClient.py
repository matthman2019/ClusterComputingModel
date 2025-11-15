from Client import Client

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

if __name__ == "__main__":
    client = Client((IP, PORT), is_mersenne_prime, 8, False, False)
    client.start()