from socket import socket , AF_INET , SOCK_STREAM
from random import seed , randint
from threading import Thread
import time
import sys

Host = '127.0.0.1'
number_of_threads = 0

#some exception that might happen

class Missing_args (Exception) :
    pass
class Fail_to_bind (Exception) :
    pass

#here is the function that the thread will start we need to past it the address
#of the server and the port number for the new socket
def Start_Game ( conn , addr , port):

    seed(1)
    print('Connected by', addr)
    conn.close()
    with socket( AF_INET, SOCK_STREAM) as s:
        s.bind((Host, port))
        s.listen()
        print("Waiting for client")
        conn , add = s.accept()
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode().split()
            print (data )
            target = randint( int(data[0]) , int(data[1]) )
            print(target)
            conn.sendall(str(target).encode())

            for i in range( 1 , 6 ) :
                print (f"waiting for attempt number {i}:")
                data = conn.recv(1024)
                if not data :
                    break
                data = int(data.decode())
                print(data)
                if data > target :
                    reply = "Your answer is bigger than the number !"
                    conn.sendall(reply.encode())
                elif data < target :
                    reply = "Your answer is lesser than the number !"
                    conn.sendall(reply.encode())
                else :
                    reply = "You Win!"
                    conn.sendall(reply.encode())
            break
        global number_of_threads
        number_of_threads -=1



try :

    # fist things first we need to check if the arguments given is just port number
    if len(sys.argv) != 2  :
        raise Missing_args
    port = int(sys.argv[1])
    port_counter = 1

    #we start the connection with main socket number given from the terminal
    with socket( AF_INET, SOCK_STREAM) as s:
        s.bind((Host, port))
        s.listen()
        #we start the server on the ip: 127.0.0.1 and the port given
        print(f"Starting the server on {Host}:{port}")
        while True:
            #now we star waiting for connections from the clints
            print("Waiting for a connection...")
            conn, addr = s.accept()
            number_of_threads+=1
            # We make sure the currently the server is handling only two clients
            if number_of_threads > 2 :
                mes = "The server is full"
                number_of_threads-=1
                conn.sendall(mes.encode())
                continue
            #if a new connection was accepted, we send the number of the new port
            mes = str(port+port_counter)
            print("Connection has been made with the clint")
            conn.sendall(mes.encode())
            #then the thread will start handling the game logic on the new socket
            thread = Thread (target= Start_Game , args= ( conn, addr , port + port_counter ,) )
            thread.start()
            port_counter +=1
except Missing_args :
    print("Usage example: python./server.py <port>")
except :
    print ("Error: unable to start thread")

