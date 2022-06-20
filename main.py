import os, threading

from azure_eventhub_reciever import SocketServer

django = threading.Thread(target=os.system, args=("python manage.py runserver 0.0.0.0:8000",))
django.daemon = True
django.start()

server = SocketServer.SocketServer(9998)
socketServer = threading.Thread(target=server.start)
socketServer.daemon = True
socketServer.start()

try:
    while True:
        pass

except KeyboardInterrupt as e:
    exit()
