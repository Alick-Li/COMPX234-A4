# Changelog

## 1st Commit
- `UDPclient/UDPclient.py`: Initial creation. Added `import socket` and `import base64`.
- `UDPclient/files.txt`: Added list of files to download (`test1.txt`, `test2.docx`, `test3.pdf`).
- `UDPserver/UDPserver.py`: Initial creation. Added imports and basic structure.
- `UDPserver/test1.txt`: Added test file with content "Hello World!".

---

## 2nd Commit
- `UDPserver/UDPserver.py`: Implemented `send_and_receive` and `download_file` stub functions for UDP server file transfer logic.

---

## 3rd Commit
- `UDPserver/UDPserver.py`: Added logic to `download_file` for receiving file content in blocks and writing to file.

---

## 4th Commit
- `UDPserver/UDPserver.py`: Improved retry logic in `send_and_receive`. Enhanced file writing and progress printing in `download_file`. Added base64 decoding and chunk handling.

---

## 5th Commit
- `UDPclient/UDPclient.py`: Added client-side implementations for `send_and_receive` and `download_file`, including retry logic and file writing with download progress.
- `UDPserver/UDPserver.py`: Refactored major logic. Moved file transfer handling into `handle_client`. Implemented block/chunk reading and transmission with error handling.

---

## 6th Commit
- `UDPclient/UDPclient.py`: Added CLI `main()` function parsing arguments, reading file list, and downloading files in a loop.
- `UDPserver/UDPserver.py`: Fixed typos in request parsing and improved chunk processing.

---

## 7th Commit
- `UDPclient/UDPclient.py`: Improved timeout handling, error messages, and request/response protocol for file download.
- Enhanced checks for server errors and download failures.

---

## 8th Commit
- `UDPserver/UDPserver.py`: Standardized server response format for file size and port info. Changed data block response to start with "FILE ... OK ... DATA ...".

---

## 9th Commit
- `UDPclient/UDPclient.py`: Aligned error message prefix from `"ERR"` to `"ERROR"` for consistency with server.
- `UDPserver/UDPserver.py`: Added main loop to listen for incoming download requests, spawn threads for each client, and handle errors gracefully.

---

## 10th Commit
- `UDPclient/UDPclient.py`: Refactored send/receive logic for clarity and reliability. Improved download loop with better error handling and progress output.
- `UDPserver/UDPserver.py`: Improved request parsing, error handling, and thread spawning. Standardized error responses.

---

## 11th Commit
- `UDPclient/UDPclient.py`: Further unified error messages and improved user feedback during download.
- `UDPserver/UDPserver.py`: Fixed parameter passing in threading and response sending to always use correct client address.

---

## 12th Commit
- `README.md`: Added comprehensive project overview, usage guide, and code structure documentation.
- `UDPclient/UDPclient.py`: Minor adjustment to error message parsing for server error alignment.
- `UDPserver/UDPserver.py`: Changed server error response from `"ERR"` to `"ERROR"` for consistency.
