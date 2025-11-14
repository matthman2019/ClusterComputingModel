# import asyncio
import socket
import queue
import multiprocessing
import time



# copied from here: https://stackoverflow.com/questions/48506460/python-simple-socket-client-server-using-asyncio

# options
printMode = True
acceptAllConnections = True
stopWhenSuccess = False

IP = []
try:
        IPSocket = socket.create_connection(("1.1.1.1", 80), 5)
        IP = IPSocket.getsockname()[0]
except TimeoutError:
    pass
except OSError:
    pass

print(f"IP: {IP}")
PORT = 15555
H = "H".encode()

def safePrint(*args):
    if not printMode:
        return
    for arg in args:
        print(arg)

def log_perfect_number(number : str):
    # print("Perfect number found!")
    # print(f"Prime: {successfulValue}")
    # number = int(number)
    # print(f"Perfect Number: {hex((2 ** (number - 1)) * ((2 ** number) - 1))}")

    with open("Primes.txt", 'a') as file:
        file.write(number + "\n")


safe_addresses = []
bad_addresses = []
value = 27887
successfulValue = None
valueQueue = multiprocessing.Queue()

def is_prime(number : int):
    for i in range(2, int(number ** 0.5) + 1, 1):
        if number % i == 0:
            return False
    return True

def find_new_primes():
    global value
    while True:
        if is_prime(value):
            valueQueue.put(value)
            # print(value)
        value += 2

        if valueQueue.qsize() > 1000:
            time.sleep(1)

valueProcess = multiprocessing.Process(target=find_new_primes)
valueProcess.start()

def get_next_value():
    global value, successfulValue, valueQueue
    if successfulValue and stopWhenSuccess:
        return successfulValue
    # get the next value.
    # replace this code!
    return valueQueue.get(timeout=5)

def handle_client(client : socket.socket, address, semaphore):
    global successfulValue
    with semaphore:
        safePrint(f"\nNew Client: {address}")
        
        if not acceptAllConnections:
            # reject bad addresses
            if address in bad_addresses:
                client.close()
            
            # see if we add a new safe address
            if not address in safe_addresses:

                acceptNewConn = input(f"New connection from {address}! Accept connection? y/n\n")
                try:
                    acceptNewConn = acceptNewConn.lower()
                    if acceptNewConn == "n":
                        bad_addresses.append(address)
                        client.close()
                    else:
                        safe_addresses.append(address)
                except:
                    client.close()

        
        print("Received")
        request =  client.recv(255).decode()

        # process request
        if request == "":
            client.close()

        match request[0]:
            case "N":
                try:
                    client.sendall(str(get_next_value()).encode())
                    safePrint(f"Successfully dealt with client {address}")
                except BrokenPipeError:
                    safePrint("Broken pipe error. Maybe worry about this?")
            case "S":
                successfulValue = request[1:]

                # changed for perfect numbers
                log_perfect_number(successfulValue)

        
        client.close()

def run_server():
    safePrint("Starting server...")
    server = socket.create_server((IP, PORT))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.listen()

    safePrint("Server is up!")


    safePrint("Listening...")
    threadList = []
    semaphore = multiprocessing.Semaphore(5)
    while True:
        client, address = server.accept()
        process = multiprocessing.Process(target=handle_client, args=(client, address[0], semaphore))
        threadList.append(process)
        process.start()

run_server()