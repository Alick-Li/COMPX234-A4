import socket
import base64
import threading
import random
import os

def handle_client(client_address, server_port, filename):
    try:
        client_port = random.randint(50000, 51000)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.bind(('', client_port))

        file_size = os.path.getsize(filename)
        response = f"OK {filename} SIZE {file_size} PORT {client_port}"
        client_socket.sendto(response.encode(), client_address)

        with open(filename, 'rb') as f:
            while True:
                request, _ = client_socket.recvfrom(1024)
                client_request = request.decode().strip()
                parts = client_request.split(" ")

                if parts[0] == "FILE" and parts[2] == "CLOSE":
                    response = f"FILE {filename} CLOSE_OK"
                    client_socket.sendto(response.encode(), client_address)
                    break
                elif parts[0] == "FILE" and parts[2] == "GET":
                    start = int(parts[4])
                    end = int(parts[6])
                    f.seek(start)
                    data = f.read(end - start + 1)
                    base64_data = base64.b64encode(data).decode()
                    response = f"FILE {filename} OK START {start} END {end} DATA {base64_data}"
                    client_socket.sendto(response.encode(), client_address)

        client_socket.close()
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except ValueError:
        print(f"Invalid request format: {client_request}")
    except Exception as e:
        print(f"Error in file transmission: {e}")

def main():
    if len(os.sys.argv) != 2:
        print("Usage: python UDPserver.py <port>")
        return

    server_port = int(os.sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', server_port))
    print(f"Server started on port {server_port}")

    while True:
        try:
            request, client_address = server_socket.recvfrom(1024)
            client_request = request.decode().strip()
            parts = client_request.split(" ")

            if parts[0] == "DOWNLOAD":
                filename = parts[1]
                if os.path.exists(filename):
                    threading.Thread(target=handle_client, args=(client_address, server_port, filename)).start()
                else:
                    response = f"ERR {filename} NOT_FOUND"
                    server_socket.sendto(response.encode(), client_address)
        except IndexError:
            print(f"Invalid request format: {client_request}")
        except Exception as e:
            print(f"Error in server loop: {e}")

if __name__ == "__main__":
    main()