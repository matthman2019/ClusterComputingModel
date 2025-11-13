# Cluster Computing Model

This project will basically be a module / API for simple cluster computing.
It's currently coded in python, but identical servers could be coded in a compiled language to increase performance.


# API

In essence: the server will generate values that each client will check.
Think of it like brute forcing a password: the server will generate strings, and the clients will check the hashes of the passwords to the known hash value.

When a client first contacts the server, the server will check with the user that the client is valid and can be let into the network.
(This is to prevent sabotaging.)
The client will send a TCP request to the server for a new value, and the server will return it.
The client can also send a "Success!" message to the server to tell it that a value has been found.
The server will then send this value to other clients. If more than half of clients validate


## Codes:

N = NEW : from client to server. This is a client asking for a new value to test.
S + ... = SOLVED : from client to server. A value has been solved! After the S, immediately add the value. So for a value 123, the client sends S123.

The server cannot send anything to the client; when a value has been solved for, the server will tell clients to solve for the correct value.
Clients can halt once they solve a value that works.