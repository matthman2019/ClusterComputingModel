# Server class for the client/server cluster computing model
import socket
import multiprocessing
from multiprocessing.shared_memory import SharedMemory
from typing import Callable, Generator
import tkinter

# Source - https://stackoverflow.com/a/28950776
# Posted by fatal_error, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-14, License - CC BY-SA 4.0
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('1.1.1.1', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Server class
class Server:

    def __init__(self,
                ip_tuple : tuple[str, int] = ("127.0.0.1", 15555),
                semaphore : multiprocessing.Semaphore = None, # type: ignore

                get_next_value_callback : Callable[[], str] = None,
                log_success_callback : Callable[[str], None] = None,

                print_mode : bool = True,
                accept_all_connections : bool = True,
                stop_when_success : bool = False,
                reusable_socket : bool = True):
        """Creates a server for a computer cluster.\n
        ip_tuple is a tuple of (IP, PORT). By default, it's on localhost and port 15555. \n
        semaphore is a multiprocessing.Semaphore object. It prevents too many clients from overloading the server. \n
        get_next_value_callback is a callback that returns a value. This value will be passed to the next client. (Generators could be helpful!) \n
        log_success_callback is a callback that logs how a successful value should be saved.
        print_mode is whether most things are printed to the console or not.
        accept_all_connections is whether all incoming computers are automatically accepted as legit clients or not.
        stop_when_success is whether or not the server will stop creating and sending new values to clients once a successful value is found.
        reusable_socket is whether the socket is reusable (just keep it True. It won't hurt anything.)
        """
        
        if get_next_value_callback is None:  
            get_next_value_callback = lambda : 0
        if log_success_callback is None:
            log_success_callback = lambda string: print(f"Success! Value: {string}")
        
        self.ip_tuple : tuple[str, int] = ip_tuple
        self.semaphore = semaphore

        self.get_next_value_callback : Callable[[], str] = get_next_value_callback
        self.log_success_callback : Callable[[str], None] = log_success_callback

        self.print_mode : bool = print_mode
        self.accept_all_connections : bool = accept_all_connections
        self.stop_when_success : bool = stop_when_success
        self.reusable_socket : bool = reusable_socket

        self.safe_addresses = []
        self.bad_addresses = []
        self.successful_values = []
    
    def __reduce__(self):
        return (self.__class__, (
                self.ip_tuple,
                self.semaphore,

                self.get_next_value_callback,
                self.log_success_callback,

                self.print_mode,
                self.accept_all_connections,
                self.stop_when_success,
                self.reusable_socket))
    
    def _safe_print(self, *args):
        if not self.print_mode:
            return
        
        for arg in args:
            print(arg, end=" ")
        print()
    
    def _get_next_value(self):
        if self.successful_values and self.stop_when_success:
            return self.successful_values
        # get the next value.
        # replace this code!
        last_value = self.get_next_value_callback()
        return last_value

    def _is_address_ok(self, address : str) -> bool:
        if self.accept_all_connections:
            return True
        # reject bad addresses
        if address in self.bad_addresses:
            return False
        # accept good addresses
        if address in self.safe_addresses:
            return True
        
        # we haven't seen this address before. See what to do with it
        acceptNewConn = input(f"New connection from {address}! Accept connection? y/n\n").lower()
        if acceptNewConn == "n":
            self.bad_addresses.append(address)
            return False
        else:
            self.safe_addresses.append(address)
            return True
    
    def _handle_client(self, client : socket.socket, address, semaphore : multiprocessing.Semaphore): # type: ignore
        """Handles a client."""
        self._safe_print(f"\nNew Client: {address}")

        # obey the semaphore
        if semaphore:
            semaphore.acquire()
        
        # check whether address is safe or not
        if not self._is_address_ok(address):
            client.close()
            return
        
        request = client.recv(255).decode()
        print(request)

        # process request

        match request[0]:
            case "N":
                client.sendall(str(self._get_next_value()).encode())
                self._safe_print(f"Successfully dealt with client {address}")

            case "S":
                # success! add this to the list and log it (if a callback was given)
                successfulValue = request[1:]
                self.successful_values.append(successfulValue)
                self.log_success_callback(successfulValue)
        
        

        
        client.close()
        if semaphore:
            semaphore.release()

    def run(self):
        """Runs the server. This is a blocking call."""
        self._safe_print("Starting server...")
        server = socket.create_server(self.ip_tuple)
        if self.reusable_socket:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.listen()

        self._safe_print(f"Server is up on {self.ip_tuple}! Listening...")

        processList = []
        try:
            while True:
                client, address = server.accept()
                process = multiprocessing.Process(target=self._handle_client, args=(client, address[0], self.semaphore))
                processList.append(process)
                process.start()
        except Exception as e:
            print(e)

    
    def start(self):
        """Creates a Process to run Server.run() in. This is a non-blocking call."""
        self.server_process = multiprocessing.Process(target=self.run)
        self.server_process.start()
    
    def run_with_graphics(self):
        self.start()
        print("Graphics are not yet implemented")
        '''
        tk = tkinter.Tk()
        value_label = tkinter.Label(tk, text=f"Last value: {self.last_value}")
        value_label.pack()

        def refresh_tk():
            last_value = memoryview(SharedMemory(name="last_value").buf)[0]
            value_label.config(text=f"Last value: {last_value}")
            tk.after(1000, refresh_tk)
        tk.after(1000, refresh_tk)

        tk.mainloop()
        print("ended")
        '''
        

    
    def queue_mode(self):
        """Set get_next_value_callback to a function that just gets from the queue. 
        You will need to put items in the queue yourself."""
        self.value_queue = multiprocessing.Queue()
        self.get_next_value_callback = self.value_queue.get
        return self.value_queue
    
    def set_ip_to_private_ip(self):
        self.ip_tuple = (get_ip(), self.ip_tuple[1])