# UDP File Transfer Client/Server System

## 1. Project Overview
A UDP-based client/server system for file downloads. Clients request files, and the server sends them in blocks via threads.

## 2. Function Introduction

### 2.1 UDPClient
1. Binds to a port and listens for DOWNLOAD requests.
2. Spawns threads to handle clients, sending file metadata and blocks.
3. Handles errors (e.g., file not found) and closes connections gracefully.

### 2.2 UDPServer
1. Reads file lists from a text file and sends DOWNLOAD requests.
2. Downloads files in blocks with retries for timeouts.
3. Uses exponential backoff for reliability.

## 3. Usage Guide

### 3.1 Start the Server
Execute in the terminal:
```bash
python UDPserver.py <port>
```
For example:
```bash
python UDPserver.py 54321
```

### 3.2 Start the Client
Execute in another terminal:
```bash
python UDPclient.py <hostname> <port> <filelist>
```
For example:
```bash
python UDPclient.py localhost 54321 files.txt
```

## 4. Code Structure

### 4.1 `UDPclient.py`
1. `send_and_receive()`: Sends requests with retries.
2. `download_file()`: Manages file download process.
3. `main()`: Parses arguments and processes file list.

### 4.2 `UDPserver.py`
1. `handle_client()`: Thread function for sending file blocks.
2. `main()`: Binds socket and spawns threads for clients.