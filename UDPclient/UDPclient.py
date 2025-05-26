import socket
import base64

def send_and_receive(socket, address, port, message):
    timeout = 1000
    retry_count = 0

    while retry_count < 5:
        try:
            socket.settimeout(timeout / 1000)
            socket.sendto(message.encode(), (address, port))
            response, _ = socket.recvfrom(2048)
            return response.decode()
        except socket.timeout:
            retry_count += 1
            timeout *= 2
    
    return None

def download_file(socket, address, port, filename):
    response = send_and_receive(socket, address, port, f"DOWNLOAD {filename}")

    if response.startswith("OK"):
        file_size = int(response.split()[3])
        data_port = int(response.split()[5])

        with open(filename, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_size:
                start = bytes_received
                end = min(start + 999, file_size - 1)

                response = send_and_receive(socket, address, data_port, f"GET {filename} {start} {end}")

                if response.startswith("FILE"):
                    return False
            
                data_start = response.find("DATA") + 5
                base64_data = response[data_start:]
                file_data = base64.b64decode(base64_data)
                f.seek(start)
                f.write(file_data)
                bytes_received += len(file_data)
                print('*', end='')

            close_response = send_and_receive(socket, address, port, f"CLOSE {filename}")
            if close_response and close_response.startswith("FILE") and "CLOSE_OK" in close_response:
                print("\nFile download completed successfully.")
                return True

        return False
