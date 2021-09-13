import socket
from os import stat


dest_ip = "127.0.0.1"
dest_port = 123456

client_ip = "127.0.0.1"
client_port = 65431


def send_message(sock, message, timeout, retries):
    global dest_ip, dest_port
    for i in range(retries):
        try:
            sock.sendto(message, (dest_ip, dest_port))
            sock.settimeout(timeout)
            s_message = sock.recvfrom(buff_size)[0].decode()
            return s_message.split("|")
        except Exception as e:
            print(e)

    return None


def fix(num):
    assert 0 <= num <= 99999
    ret = '0' * 4 + str(num)
    return ret[-5:]


file_name = './example.png'
f = open(file_name, 'rb')
file_size = stat(file_name).st_size
file_extension = file_name.split(".")[-1]

buff_size = 2048
seq0 = 0

client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Generating and sending the message to the server.
start_message = ("s|" + fix(seq0) + "|" + file_extension + "|" + str(file_size)).encode()
print("Starting transfer.")
s_message_elems = send_message(client_socket, start_message, .5, 5)

# Stopping the process if the server does not respond.
if s_message_elems is None:
    print("The sever is not responding to the start message! Shutting down...")
    client_socket.close()
    exit(0)


max_size = 0
cur_seq_n = 0

# Checking the correctness of the received message.
try:
    assert len(s_message_elems) == 3 and s_message_elems[0] == 'a' and int(s_message_elems[1]) == cur_seq_n + 1
    max_size = int(s_message_elems[-1])
    cur_seq_n += 1
except Exception as e:
    print("Invalid response to the start message! Shutting down...")
    client_socket.close()
    exit(0)

header_size = 8

# Transmitting the actual file.
data = f.read(max_size - header_size)
while data:
    message = f'd|{fix(cur_seq_n)}|'.encode() + data
    s_message_elems = send_message(client_socket, message, 0.5, 5)

    if s_message_elems is None:
        print(f"Ack timeout. Cancelling transfer.")
        client_socket.close()
        exit(0)
    try:
        assert len(s_message_elems) == 2 and s_message_elems[0] == 'a' and int(s_message_elems[1]) == cur_seq_n + 1
        cur_seq_n += 1
    except Exception as e:
        print(f"Invalid response")
        client_socket.close()
        exit(1)
    data = f.read(max_size - header_size)

print("File transfer successful.")
client_socket.close()
