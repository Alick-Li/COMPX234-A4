import socket
import base64
import sys
import os

def send_and_receive(socket, address, port, message, max_retries=5, initial_timeout=1000):
    current_timeout = initial_timeout
    retries = 0
    while retries < max_retries:
        try:
            socket.settimeout(current_timeout / 1000)
            socket.sendto(message.encode(), (address, port))
            response, _ = socket.recvfrom(2048)
            return response.decode().strip()
        except TimeoutError:
            retries += 1
            current_timeout *= 2
            print(f"Timeout, retrying... (attempt {retries})")
        except Exception as e:
            print(f"Error in send_and_receive: {e}")
            break
    return None

def download_file(socket, address, port, filename):
    response = send_and_receive(socket, address, port, f"DOWNLOAD {filename}")

    if response is None:
        print(f"Failed to download {filename}: No response from server.")
        return False
    elif response.startswith("ERROR"):
        print(f"Server error: {response}")
        return False
    elif response.startswith("OK"):
        try:
            parts = response.split(" ")
            file_size = int(parts[3])
            data_port = int(parts[5])

            print(f"Downloading {filename} (size: {file_size} bytes)", end='', flush=True)

            with open(filename, 'wb') as f:
                bytes_received = 0
                block_size = 1000

                while bytes_received < file_size:
                    start = bytes_received
                    end = min(start + block_size - 1, file_size - 1)

                    request = f"FILE {filename} GET START {start} END {end}"
                    response = send_and_receive(socket, address, data_port, request)

                    if response is None or not response.startswith("FILE") or "OK" not in response:
                        print(f"\nError receiving data for {filename}")
                        return False

                    data_start = response.find("DATA") + 5
                    base64_data = response[data_start:]
                    file_data = base64.b64decode(base64_data)
                    f.seek(start)
                    f.write(file_data)
                    bytes_received += len(file_data)
                    print('*', end='', flush=True)

                close_response = send_and_receive(socket, address, data_port, f"FILE {filename} CLOSE")
                if close_response and close_response.startswith("FILE") and "CLOSE_OK" in close_response:
                    print(f"\nSuccessfully downloaded {filename}")
                    return True
        except (IndexError, ValueError) as e:
            print(f"Error parsing server response for {filename}: {e}")
            return False

    return False

def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <hostname> <port> <filelist>")
        return

    server_address = sys.argv[1]
    server_port = int(sys.argv[2])
    file_list = sys.argv[3]

    if not os.path.exists(file_list):
        print(f"File list {file_list} not found")
        return

    with open(file_list, 'r') as f:
        files = [line.strip() for line in f if line.strip()]

    if not files:
        print("No files specified in the file list")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for file_name in files:
        download_file(client_socket, server_address, server_port, file_name)

    client_socket.close()

if __name__ == "__main__":
    main()