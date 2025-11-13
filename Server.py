import asyncio
import socket

# copied from here: https://stackoverflow.com/questions/48506460/python-simple-socket-client-server-using-asyncio

# options
printMode = True
acceptAllConnections = True
stopWhenSuccess = False


# codes
H = "H".encode()

def safePrint(*args):
    if not printMode:
        return
    for arg in args:
        print(arg)

safe_addresses = []
bad_addresses = []

value = 0
successfulValue = None
async def get_next_value():
    global value, successfulValue
    if successfulValue and stopWhenSuccess:
        return successfulValue
    # get the next value.
    # replace this code!
    value += 1
    return value

async def handle_client(client, address):
    global successfulValue
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
    
    loop = asyncio.get_event_loop()

    request = (await loop.sock_recv(client, 255)).decode()

    # process request
    if request == "":
        client.close()

    match request[0]:
        case "N":
            try:
                await loop.sock_sendall(client, str(await get_next_value()).encode())
                safePrint(f"Successfully dealt with client {address}")
            except BrokenPipeError:
                safePrint("Broken pipe error. Maybe worry about this?")
        case "S":
            successfulValue = request[1:]
            safePrint(f"Client {address} reported a successful value! Value: {successfulValue}")

    
    client.close()

async def run_server():
    safePrint("Starting server...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 15555))
    server.listen()
    server.setblocking(False)

    safePrint("Server is up!")

    loop = asyncio.get_event_loop()

    safePrint("Listening...")
    while True:
        client, address = await loop.sock_accept(server)
        loop.create_task(handle_client(client, address[0]))

asyncio.run(run_server())