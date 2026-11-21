import socket
import sys

def scan_ports(target_host, start_port, end_port):
    """
    Scan a range of ports on target_host.
    Prints OPEN ports, and a summary at the end.
    Handles connection errors gracefully.
    """
    print(f"Scanning {target_host} from port {start_port} to {end_port}...")
    print("-" * 50)

    open_ports = []

    for port in range(start_port, end_port + 1):
        # Create a new TCP socket for each port
        # AF_INET = IPv4, SOCK_STREAM = TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Don't hang if host doesn't respond

        try:
            # connect_ex() returns 0 if connection succeeds (port open)
            # instead of raising an exception like connect()
            result = sock.connect_ex((target_host, port))

            if result == 0:
                print(f"Port {port}: OPEN")
                open_ports.append(port)
            else:
                print(f"Port {port}: closed")

        except socket.gaierror:
            # Hostname could not be resolved
            print(f"Error: Could not resolve hostname '{target_host}'")
            sock.close()
            return
        except socket.error as e:
            # Connection error - e.g. inactive server / host down
            print(f"Error: Could not connect to {target_host}:{port} - {e}")
        except KeyboardInterrupt:
            # Allow user to stop scan cleanly with Ctrl+C
            print("\nScan interrupted by user. Exiting gracefully...")
            sock.close()
            break
        finally:
            # Graceful disconnection: always close the socket
            # This prevents leaving half-open connections behind
            try:
                sock.close()
            except Exception:
                pass

    # Summary at the end
    print("-" * 50)
    if open_ports:
        print(f"Scan complete. Open ports: {open_ports}")
    else:
        print("Scan complete. No open ports found in this range.")

def main():
    """Parse command-line arguments, validate them, then run the scan."""

    # 1. Check correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: python3 port_scanner.py <target_host> <start_port> <end_port>")
        print("Example: python3 port_scanner.py 127.0.0.1 1 100")
        sys.exit(1)

    target_host = sys.argv[1]

    # 2. Ports must be numbers
    try:
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])
    except ValueError:
        print("Error: Ports must be numbers")
        print("Example: python3 port_scanner.py 127.0.0.1 1 100")
        sys.exit(1)

    # 3. Validate port range: 1-65535, start <= end
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print(f"Error: Invalid port range - {start_port}-{end_port}")
        print("Ports must be between 1 and 65535, and start must be <= end")
        sys.exit(1)

    # 4. Security check: only allow authorized targets
    allowed_hosts = ["127.0.0.1", "localhost", "scanme.nmap.org"]
    if target_host not in allowed_hosts:
        print(f"Error: Scanning '{target_host}' is not authorized for this assignment.")
        print(f"Only allowed: {', '.join(allowed_hosts)}")
        sys.exit(1)

    # 5. All checks passed - run the scan
    scan_ports(target_host, start_port, end_port)

if __name__ == "__main__":
    main()