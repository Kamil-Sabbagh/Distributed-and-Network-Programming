import pickle
import sys
import os
import xmlrpc.client
import argparse

parser = argparse.ArgumentParser(usage='Usage example: python./server.py <port>')
parser.add_argument('host', type=str, help='Address')
parser.add_argument('port', type=int, help='port to run the server on')
args = parser.parse_args()

s = xmlrpc.client.ServerProxy(f'http://{args.host}:{args.port}')

while True:
    try:
        command = input("\nEnter the command:\n")

        command_parts = command.split()

        if command_parts[0] == 'send':
            if not os.path.exists('./client_folder/' + command_parts[1]):
                print("Not completed")
                print("File doesn't exist")
            else:
                with open('./client_folder/' + command_parts[1], 'rb') as f:
                    bytes = pickle.dumps(f.read())
                    data = s.send(command_parts[1], bytes)
                if data == True:
                    print("Completed")
                else:
                    print("Not completed")
                    print("File already exists")

        elif command_parts[0] == 'list':
            data = s.list()
            for x in range(len(data)):
                print(data[x])
            # print("\n".join(data))
            print("Completed")

        elif command_parts[0] == 'delete':
            data = s.delete(command_parts[1])
            if data == True:
                print("Completed")
            else:
                print("Not completed")
                print("No such file")

        elif command_parts[0] == 'get':
            status, bytes = s.get(command_parts[1])

            # When a user doesn't want to change the name of the file
            if len(command_parts) == 2:
                if os.path.exists("./client_folder/" + command_parts[1]):
                    print("Not completed")
                    print("File already exists")

                elif status == False:
                    print("Not completed")
                    print("File doesn't exist on the server")

                elif status == True:
                    with open("./client_folder/" + command_parts[1], 'wb') as file:
                        file.write(pickle.loads(bytes.data))
                        print("Completed")

            # When a user wants to change the name of the file
            elif len(command_parts) == 3:

                if os.path.exists("./client_folder/" + command_parts[2]):
                    print("Not completed")
                    print("File already exists")

                elif status == False:
                    print("Not completed")
                    print("File doesn't exist on the server")
                elif status == True:
                    with open(f"./client_folder/{command_parts[2]}", 'wb') as file:
                        file.write(pickle.loads(bytes.data))
                        print("Completed")

        elif command_parts[0] == 'calc':
            data, status = s.calc(command)

            if status:
                print(int(data))
                print("Completed")
            else:
                print("Not completed")
                print(data)

        elif command == "quit":
            print("Client is stopping")
            exit()

        else:
            print("Not completed\nWrong command")

    except KeyboardInterrupt:
        print("Server is stopping")
        exit()

    except IndexError:
        print("Not completed\nWrong command")

    except ConnectionRefusedError:
        print("Server unreachable")
        exit()
    except ValueError:
        print("Not completed\nWrong command")
