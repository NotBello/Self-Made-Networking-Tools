import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 53)

    while True:
        hostname = input("Enter hostname/alias: ")
        client_socket.sendto(hostname.encode(), server_address)

        response, _ = client_socket.recvfrom(1024)
        print(response.decode())

        choice = input("Do you want to continue? (y/n): ")
        if choice.lower() != 'y':
            break
    
    client_socket.close()

if __name__ == "__main__":
    main()
