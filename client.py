import socket

# Must match the server's host and port
HOST = '127.0.0.1'
PORT = 5001

# Create a TCP socket: AF_INET = IPv4, SOCK_STREAM = TCP
# Using 'with' ensures the socket closes automatically
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Stop waiting after 5 seconds if the server doesn't respond
    client_socket.settimeout(5)
    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        # Send a message to the server
        client_socket.sendall(b"Hello Server!")
        # Wait for and print the server's response
        response = client_socket.recv(1024)
        print(f"Received: {response.decode()}")
    except ConnectionRefusedError:
        # Server is not running
        print("Could not connect: Is the server running?")
    except socket.timeout:
        # Server took too long to respond
        print("Connection timed out")
    except OSError as e:
        # Any other socket error
        print(f"Socket error: {e}")