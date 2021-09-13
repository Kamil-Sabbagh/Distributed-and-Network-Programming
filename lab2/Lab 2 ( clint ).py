DEST_IP_ADDR = '127.0.0.1'
DEST_PORT = 65432
PORT = 65433
BUF_SIZE = 100

from socket import socket , AF_INET , SOCK_DGRAM

s = socket(AF_INET , SOCK_DGRAM )

s.bind(("Localhost" , PORT))

while True :
    message = input("enter the equation \n")
    s.sendto( message.encode() , (DEST_IP_ADDR , DEST_PORT) )
    if message.lower() == "quit" :
        print("User has quit!")
        break
    data , addr = s.recvfrom(BUF_SIZE)
    print(data)


s.close()
