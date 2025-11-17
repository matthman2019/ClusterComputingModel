import multiprocessing
from Server import Server, get_ip
import time

def log_new_prime(string : str):
    print(f"Success! Power: {string}")
    with open("Primes2.txt", "a") as file:
        file.write(string + '\n')

server = Server(ip_tuple=(get_ip(), 15555), print_mode=True, log_success_callback=log_new_prime)
valueQueue = server.queue_mode()

def is_prime(number : int):
    for i in range(2, int(number ** 0.5) + 1, 1):
        if number % i == 0:
            return False
    return True

value = 108959
def find_new_primes():
    global value
    while True:
        if is_prime(value):
            valueQueue.put(value)
        value += 2

        while valueQueue.qsize() > 1000:
            time.sleep(1)



valueProcess = multiprocessing.Process(target=find_new_primes)
valueProcess.start()

server.start()
# last: Testing 111733
