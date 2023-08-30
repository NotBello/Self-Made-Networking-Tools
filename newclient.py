import socket
def commands_help():
    print("The commands")

def dns_lookup(dns_client_socket, destination_address):
    dns_lockon = "dnslookup"
    dns_client_socket.sendto(dns_lockon.encode(), destination_address)
    
    hostname = input("Enter hostname/alias: ")
    dns_client_socket.sendto(hostname.encode(), destination_address)

    response, _ = dns_client_socket.recvfrom(1024)
    print(response.decode())

def list_records(dns_client_socket, destination_address):
    dns_lockon = "dnslist"
    dns_client_socket.sendto(dns_lockon.encode(), destination_address)

    data, addr = dns_client_socket.recvfrom(1024)
    received_table = data.decode()
    print("Received data:\n", received_table)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 53)

    while True:
        option = input("Enter command : ")
        formated_option = option.lower()
        match formated_option:
            case "/help":
                commands_help()
            case "/list":
                list_records(client_socket, server_address)
            case "/lookup":
                dns_lookup(client_socket, server_address)
            case "/add":
                dns_add()
            case "/remove":
                dns_remove()
            case "/exit":
                exit_program()

        choice = input("Do you want to continue? (y/n): ")
        if choice.lower() != 'y':
            break
    
    client_socket.close()

if __name__ == "__main__":
    main()



                