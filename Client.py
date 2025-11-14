# Client class
# clients can connect to servers, yada yada
import socket
import multiprocessing
from typing import Callable
    


# a client for the client/server cluster computing model.
# ip_tuple is a tuple of (IP, PORT).
# evaluate_function evaluates whether a given value (a string) is successful or not. It is passed as the target argument into multiprocessing.Process.()
# number_of_processes is how many multiprocessing.Process() processes to make.
class Client:

    N = "N".encode()

    def __init__(self, ip_tuple : tuple[str, int], 
                evaluate_function : Callable[[str], bool], 
                number_of_processes : int = 1, 
                stop_when_success : bool = False, 
                print_mode : bool = True):
        
        self._ipTuple : tuple[str, int] = ip_tuple
        self._ip, self._port = ip_tuple
        self.evaluate_function : Callable[[str],bool] = evaluate_function
        self.number_of_processes : int = number_of_processes
        self.stop_when_success : bool = stop_when_success
        self.print_mode : bool = print_mode
    
    # starts the Client. 
    # spawns number_of_processes processes.
    # this still needs to be put in "if __name__ == '__main__'"
    def start(self):
        
        self.process_list = []
        for i in range(self.number_of_processes):
            new_process = multiprocessing.Process(target=self._do_client_stuff)
            new_process.start()
            self.process_list.append(new_process)

    @property
    def ip_tuple(self):
        return self._ipTuple

    @ip_tuple.setter
    def ipTuple(self, newTuple : tuple[str, int]):
        self._ipTuple = newTuple
        self._ip, self._port = newTuple
    
    @property
    def ip(self):
        return self._ip
    
    @ip.setter
    def ip(self, newIP : str):
        self._ip = newIP
        self._ipTuple = (newIP, self._ipTuple[1])

    @property
    def port(self):
        return self._port
    
    @port.setter
    def port(self, newPort : int):
        self._port = newPort
        self._ipTuple = (self._ipTuple[0], newPort)

    # methods when running

    # prints, but only if self.print_mode is True
    def _safe_print(self, string : str) -> None:
        if not self.print_mode:
            return
        print(string)

    def _get_new_value(self) -> str:
        conn = socket.create_connection(self._ipTuple)
        conn.send(Client.N)
        return (conn.recv(2048).decode())

    def _report_solved_value(self, value : str) -> None:
        conn = socket.create_connection(self._ipTuple)
        conn.send(("S" + value).encode())

    def _do_client_stuff(self):
        print("Go")
        while True:
            value = self._get_new_value()
            self._safe_print(f"Testing {value}")

            if not self.evaluate_function(value):
                continue
            
            self._safe_print(f"Successful value found! Value: {value}")
            self._report_solved_value(value)
    
    
    


