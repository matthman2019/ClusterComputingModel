import socket
import time

N = "N".encode()

IP = "127.0.0.1"
PORT = 15555

def get_new_value() -> str:
    conn = socket.create_connection((IP, PORT))
    conn.send(N)
    return (conn.recv(2048).decode())

def report_solved_value(value : str) -> None:
    conn = socket.create_connection((IP, PORT))
    conn.send(("S" + value).encode())
    
def evaluate_value(value : str) -> bool:
    # replace this code with whatever needs to be done to validate the value
    return value == "10000"

startTime = time.perf_counter()

while True:
    value = get_new_value()
    if not evaluate_value(value):
        continue
    
    print(f"Successful value found! Value: {value}")
    report_solved_value(value)
    break

endTime = time.perf_counter()

print(endTime - startTime)
