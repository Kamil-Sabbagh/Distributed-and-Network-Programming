from socket import socket , AF_INET , SOCK_STREAM
import sys
import time

#some exception that might happen

class Missing_args (Exception) :
    pass



try :
    #first things first, we make sure we have only two arguments, the ip address and the port number
    if len(sys.argv) != 3  :
        raise Missing_args
    Host = sys.argv[1]
    Port = int(sys.argv[2])
    #we start by getting access the server main socket
    with socket (AF_INET, SOCK_STREAM) as s:
        s.connect((Host, Port ))
        ack = s.recv(1024)
        ack = ack.decode()
        print(ack)
        if ack == "The server is full" :
            print(ack)
        else :
            with socket (AF_INET, SOCK_STREAM) as ss :
                time.sleep(2)
                #after getting access to the server, the server will send a new port number
                #for the new socket
                ss.connect( (Host , int(ack) ) )
                print("Connection has been made with the server")
                # now a new socket has been made and connected with the sever
                input_is_ok = False
                message = ""
                #next we need to make sure that the range given is valid
                while not input_is_ok :
                    message = (input("Enter the range:\n"))
                    The_range = message.split()
                    if len(The_range) == 2 and int(The_range[0]) < int(The_range[1]):
                        input_is_ok = True

                #we send the valid range to the server
                ss.send(message.encode())
                data = ss.recv(1024)

                print("Start guessing you have 5 guesses !")
                win = False

                for i in range(1 , 6) :
                    #here is where the client will send guess back and forth with the server
                    #trying to guess the number
                    attempt = input(f"input your guess number {i}:\n")
                    ss.sendall(attempt.encode())
                    reply = ss.recv(1024)
                    reply = reply.decode()
                    print(reply)
                    if reply == "You Win!" :
                        win = True
                        break

                if win == False :
                    print("You lost")

except Missing_args :
    print("Usage example: python./client.py <address> <port>")

except:
     print("Server is unavailable")
