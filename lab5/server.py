import sys
import pickle
import os
from xmlrpc.server import SimpleXMLRPCServer
import argparse

parser = argparse.ArgumentParser(usage='Usage example: python./server.py <port>')
parser.add_argument('host', type=str, help='Address')
parser.add_argument('port', type=int, help='port to run the server on')
args = parser.parse_args()

# Main server code
with SimpleXMLRPCServer((args.host, args.port)) as server:
    try:
        def send(name, data):
            status = False
            if os.path.exists("./server_folder/" + name):
                print(name + " not saved")
            else:
                with open("./server_folder/" + name, 'wb') as file:
                    file.write(pickle.loads(data.data))
                    status = True
                    print(name + " saved")
            return status

        server.register_function(send, 'send')


        def list():
            return os.listdir("./server_folder")

        server.register_function(list, 'list')


        def delete(name):
            status = False
            try:
                os.remove("./server_folder/" + name)
                status = True
                print(name + " deleted")
                return status
            except FileNotFoundError:
                print(name + " not deleted")
                return status

        server.register_function(delete, 'delete')


        def get(name):
            status = False
            file = ""
            try:
                with open('./server_folder/' + name, 'rb') as f:
                    file = pickle.dumps(f.read())
                    status = True
            except FileNotFoundError:
                print("No such file: " + name)
            return status, file

        server.register_function(get, 'get')


        def calc(expression):
            status = False
            exp = expression.split()
            sign = exp[1]
            num1 = exp[2]
            num2 = exp[3]

            try:
                if sign == '+':
                    answ = int(num1) + int(num2)
                    status = True
                    print(expression + " -- done")

                elif sign == '-':
                    answ = int(num1) - int(num2)
                    status = True
                    print(expression + " -- done")

                elif sign == '*':
                    answ = int(num1) * int(num2)
                    status = True
                    print(expression + " -- done")

                elif sign == '/':
                    try:
                        answ = int(num1) / int(num2)
                        status = True
                        print(expression + " -- done")
                    except ZeroDivisionError:
                        print(expression + " -- not done")
                        answ = "Division by zero"

                elif sign == '>':
                    answ = int(num1) > int(num2)
                    status = True
                    print(expression + " -- done")

                elif sign == '<':
                    answ = int(num1) < int(num2)
                    status = True
                    print(expression + " -- done")

                elif sign == '>=':
                    answ = int(num1) >= int(num2)
                    status = True
                    print(expression + " -- done")

                elif sign == '<=':
                    answ = int(num1) <= int(num2)
                    status = True
                    print(expression + " -- done")

                return answ, status
            except ValueError:
                answ = "Wrong Command"
                return answ, status

        server.register_function(calc, 'calc')

        # Running the server
        server.serve_forever()

    except KeyboardInterrupt:
        print("Server is stopping")
        exit()
