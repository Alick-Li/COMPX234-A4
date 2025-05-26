import socket
import base64
import threading

def send_and_receive(socket, address, port, message):
    timeout = 1000
    retry_count = 0

    while retry_count < 5:
        socket.settimeout(timeout / 1000)
        socket.sendto(message.encode(), (address, port))
        response, _ = socket.recvfrom(2048)
        return response.decode()
    
    return None

def download_file(socket, address, port, filename):
    response = send_and_receive(socket, address, port, f"DOWNLOAD {filename}")

    if response.startswith("OK"):
        file_size = int(response.split()[3])
        data_port = int(response.split()[5])

        return True
    