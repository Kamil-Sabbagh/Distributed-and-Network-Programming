import socket
from multiprocessing import Process, Manager
import time


def delete_complete(my_dict, key_d, timeout):
    time.sleep(timeout)
    print(my_dict)
    del my_dict[key_d]
    print(my_dict)


if __name__ == '__main__':
    ip_addr = "127.0.0.1"
    port = 123456
    buff_size = 1024

    extensions = ['jpg', 'txt', 'doc', 'py', 'png']
    type_dict = dict(s='start', d='data')

    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server_socket.bind((ip_addr, port))
    with Manager() as manager:
        data_dict = manager.dict()

        while True:
            keys_list = list(data_dict)
            for i_key in keys_list:
                if time.time() - data_dict[i_key]['last_packet'] >= 3:
                    del data_dict[i_key]

            try:
                server_socket.settimeout(0.5)
                bytesAddressPair = server_socket.recvfrom(buff_size)
            except Exception as e:
                continue
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            key = address[0]
            split_list = message.split('|'.encode(), maxsplit=1)
            if len(split_list) != 2:
                print("Invalid packet.")
                continue
            message_type, rest = split_list
            message_type = message_type.decode()
            if message_type not in 'sd':
                print("Invalid packet.")
            c_message_elems = [message_type]
            message_type = type_dict[message_type]
            if message_type == 'start':
                split_list = rest.split('|'.encode(), maxsplit=2)
                if len(split_list) != 3:
                    print("Invalid message. The message will be ignored")
                    continue
                c_message_elems += [split_list[0].decode(), split_list[1].decode(), split_list[2]]
            else:
                split_list = rest.split('|'.encode(), maxsplit=1)
                if len(split_list) != 2:
                    print("Invalid message. The message will be ignored")
                    continue
                c_message_elems += [split_list[0].decode(), split_list[1]]
            # Checking the correctness of the message received message from the client.
            try:
                assert (len(c_message_elems) == 4 and c_message_elems[0] == 's' and int(c_message_elems[1]) >= 0 and
                        c_message_elems[2] in extensions and int(c_message_elems[3]) > 0) or \
                       (len(c_message_elems) == 3 and c_message_elems[0] == 'd' and int(c_message_elems[1]) > 0)
                message_type = type_dict[c_message_elems[0]]
            except Exception as e:
                print("Invalid packet")
                continue
            seq_n = int(c_message_elems[1])
            if message_type == 'start':
                if key in data_dict:
                    print("Packet is ignored.")
                    continue
                extension = c_message_elems[2]
                size = int(c_message_elems[3])
                print(f"Starting a new file transmitting session with sequence number {seq_n} and extension {extension} and of "
                       f"size {size}")
                data_dict[key] = dict(seq_n=seq_n + 1, extension=extension, size=size, data=[], cur_size=0, last_packet=time.time())
                # print('Now sending the ack message.')
                s_message = 'a|' + str(seq_n + 1) + '|' + str(buff_size)
                server_socket.sendto(s_message.encode(), address)

            elif message_type == 'data':
                # print("It's a data message")
                if key not in data_dict:
                    print("There's no active session with this client! The message is ignored.")
                    continue
                data = data_dict[key]
                if data['seq_n'] != seq_n:
                    print(f"The message's sequence number {seq_n} does not match the required one {data['seq_n']}. " +
                          "The message is ignored.")
                    continue
                if data['cur_size'] == data['size']:
                    print("The message is ignored.")
                    continue
                new_data = c_message_elems[-1]
                data['data'].append(new_data)
                data['seq_n'] = data['seq_n'] + 1
                data['cur_size'] += len(new_data)
                data['last_packet'] = time.time()
                data_dict[key] = data

                # print(f"Successfully received the packet with sequence number {seq_n}. Now sending ack message.")
                s_message = 'a|' + str(data['seq_n'])
                server_socket.sendto(s_message.encode(), address)
                if data['cur_size'] >= data['size']:
                    p = Process(target=delete_complete(data_dict, key, 5))
                    p.start()

            # print(data_dict)
