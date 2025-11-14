import socket
import multiprocessing

N = "N".encode()

IP = "10.143.14.185"
PORT = 15555

# added just for the perfect numbers task
def is_mersenne_prime(number : int):
    mersenne_number = (2 ** number) - 1
    s = 4
    for i in range(number - 2):
        s = ((s * s) - 2) % mersenne_number
    return s == 0

# change this to whatever's necessary
def evaluate_value(value : str) -> bool:
    # replace this code with whatever needs to be done to validate the value
    return is_mersenne_prime(int(value))



# don't mess with this
def get_new_value() -> str:
    conn = socket.create_connection((IP, PORT))
    conn.send(N)
    return (conn.recv(2048).decode())

# also don't mess with this
def report_solved_value(value : str) -> None:
    conn = socket.create_connection((IP, PORT))
    conn.send(("S" + value).encode())


def do_client_stuff():
    while True:
        value = get_new_value()
        if not evaluate_value(value):
            continue
        
        print(f"Successful value found! Value: {value}")
        report_solved_value(value)

if __name__ == "__main__":
    processList = []
    for i in range(8):
        process = multiprocessing.Process(target=do_client_stuff)
        process.start()
        processList.append(process)