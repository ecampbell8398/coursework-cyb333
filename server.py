import socket

# Configuration - using localhost so this only runs on your own machine
HOST = '127.0.0.1'
PORT = 5001

# Create a TCP socket: AF_INET = IPv4, SOCK_STREAM = TCP
# Using 'with' ensures the socket is closed automatically, even if an error occurs
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Allow the socket to be reused immediately after the program restarts
    # Prevents "Address already in use" errors
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind the socket to the host and port
        server_socket.bind((HOST, PORT))
        # Start listening, allow up to 5 clients to wait in the queue
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}")

        # Keep the server running to accept multiple clients, one at a time
        while True:
            # Accept a new client connection - blocks until a client connects
            conn, addr = server_socket.accept()
            # 'with conn' closes this client connection automatically when done
            with conn:
                print(f"Connected by {addr}")
                try:
                    # Receive up to 1024 bytes from the client
                    data = conn.recv(1024)
                    # If client sends nothing, they disconnected - go back to listening
                    if not data:
                        print(f"Client {addr} disconnected")
                        continue
                    print(f"Received: {data.decode()}")
                    # Send a response back to the client
                    conn.sendall(b"Hello from server!")
                except (ConnectionResetError, BrokenPipeError):
                    # Client closed the connection abruptly
                    print(f"Connection with {addr} lost")
    except KeyboardInterrupt:
        # Ctrl + C pressed - shut down cleanly instead of crashing
        print("\nServer shutting down gracefully...")
    except OSError as e:
        # Handles errors like port already in use or permission denied
        print(f"Could not start server: {e}")