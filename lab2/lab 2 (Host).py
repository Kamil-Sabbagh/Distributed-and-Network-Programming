class division_by_zero (Exception) :
    pass

class Invalid_operation(Exception) :
   pass


from socket import socket , AF_INET , SOCK_DGRAM

IP_ADDR = '127.0.0.1'
PORT = 65432
DEST_PORT = 65433
BUF_SIZE = 100

s = socket ( AF_INET , SOCK_DGRAM )

s.bind ((IP_ADDR , PORT))

print ("Waiting for a message!")
while True :
   data , addr = s.recvfrom(BUF_SIZE)
   data.lower()
   if data == b'quit' :
      print("User has quit!!")
      break
   data = data.split()
   try :
      if len(data) != 3 :
         raise Invalid_operation
      if data[0] == b'+' :
         res = float(data[1]) + float(data[2])
         if float(res) == int(res) :
            res = int(res)
         print ( res )
         res = str(res)
         s.sendto( res.encode()  , ( IP_ADDR , DEST_PORT) )
      elif data[0] == b'-' :
         res = float(data[1]) - float(data[2])
         if float(res) == int(res) :
            res = int(res)
         print ( res )
         res = str(res)
         s.sendto( res.encode()  , ( IP_ADDR , DEST_PORT) )
      elif data[0] == b'*' :
         res = float(data[1]) * float(data[2])
         if float(res) == int(res) :
            res = int(res)
         print ( res )
         res = str(res)
         s.sendto( res.encode()  , ( IP_ADDR , DEST_PORT) )
      elif data[0] == b'/' :
            if data[2] == b'0' :
               raise division_by_zero
            res = float(data[1]) / float(data[2])
            if float(res) == int(res) :
               res = int(res)
            print ( res )
            res = str(res)
            s.sendto( res.encode()  , ( IP_ADDR , DEST_PORT) )
      elif data[0] == b'>' :
         res = float(data[1]) > float(data[2])
         if float(res) == int(res) :
            res = int(res)
         print ( res )
         res = str(res)
         s.sendto( res.encode()  , ( IP_ADDR , DEST_PORT) )
      elif data[0] == b'<' :
         res = float(data[1]) < float(data[2])
         if float(res) == int(res) :
            res = int(res)
         print ( res )
         res = str(res)
         s.sendto( res.encode()  , ( IP_ADDR , DEST_PORT) )
      elif data[0] == b'>=' :
         res = float(data[1]) >= float(data[2])
         if float(res) == int(res) :
            res = int(res)
         print ( res )
         res = str(res)
         s.sendto( res.encode()  , ( IP_ADDR , DEST_PORT) )
      elif data[0] == b'<=' :
         res = float(data[1]) <= float(data[2])
         if float(res) == int(res) :
            res = int(res)
         print ( res )
         res = str(res)
         s.sendto( res.encode()  , ( IP_ADDR , DEST_PORT) )
      else:
         raise Invalid_operation
   except division_by_zero :
      res = "You are trying to divide by 0 !!"
      print(res)
      s.sendto( res.encode()  , ( IP_ADDR , DEST_PORT) )
   except Invalid_operation :
      res = "The input is Invalid !!"
      print(res)
      s.sendto( res.encode()  , ( IP_ADDR , DEST_PORT) )





   # if chr(data[0]) == '-' :
   #    print ( float(chr(data[1])) - float(chr(data[2])) )
   # if chr(data[0]) == '*' :
   #    print ( float(chr(data[1])) * float(chr(data[2])) )
   # if chr(data[0]) == '/' :
   #    print ( float(chr(data[1])) / float(chr(data[2])) )


