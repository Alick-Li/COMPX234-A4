import socket
import base64
import threading
import random
import os

def handle_client(address, port, filename):
    try:
        client_port = random.randint(50000, 51000)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.bind(('', client_port))

        file_size = os.path.getsize(filename)

        response = f"OK {filename} {file_size} {client_port}"
        client_socket.sendto(response.encode(), (address, port))

        with open(filename, 'rb') as f:
            while True:
                request, _ = client_socket.recvfrom(1024)
                client_request = request.decode()
            
                if client_request.split(" ").[0] == "FILE" and client_request.split(" ").[2] == "CLOSE":
                    response = f"FILE {filename} CLOSE_OK"
                    client_socket.sendto(response.encode(), address)
                    break
                elif client_request.split(" ").[0] == "FILE" and client_request.split(" ").[2] == "GET":
                    start = int(client_request.split(" ")[4])
                    end = int(client_request.split(" ")[6])
                    f.seek(start)
                    data = f.read(end - start + 1)
                    base64_data = base64.b64encode(data).decode()
                    response = f"DATA {filename} {start} {end} {base64_data}"
                    client_socket.sendto(response.encode(), address)
            
            client_socket.close()

    except Exception as e:
        print(f"Error handling client {address}:{port} - {e}")