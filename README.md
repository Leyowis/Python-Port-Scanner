Port Scanner in Python
This Python script performs a basic port scanning operation to detect open ports on a given IP address within a specified range. It identifies services running on common ports, such as FTP, HTTP, SSH, and MySQL, and displays information about the protocol type (TCP/UDP) and version where applicable. The script uses the socket library for network communication and ThreadPoolExecutor for concurrent scanning to speed up the process.

Features:
- Scans a range of ports on a specified IP address.
- Identifies common services (e.g., HTTP, SSH, MySQL) running on open ports.
- Detects HTTP versions (1.1/2.0) on port 80.
- Supports both TCP and UDP protocols.
- Concurrent port scanning using Python's concurrent.futures.ThreadPoolExecutor for faster results.
