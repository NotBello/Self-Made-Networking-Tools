import socket
def commands_help():
    print("/lookup   for dnslookup")
    print("/list   for listing all dns records")
    print("/add   for adding non persistent dns record data to the server")
    print("/remove   for removing non persistent dns record data from the server")
    print("/exit   for exiting console application")


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
    
def add_records(dns_client_socket, destination_address):
    dns_lockon = "dnsadd"
    dns_client_socket.sendto(dns_lockon.encode(), destination_address)

    domain = input("Enter domain: ")
    record_type = input("Enter record type (A/CNAME): ")
    value = input("Enter value: ")

    dns_record_data = f"{domain},{record_type},{value}" 
    dns_client_socket.sendto(dns_record_data.encode(), destination_address)

def remove_records(dns_client_socket, destination_address):
    dns_lockon = "dnsremove"
    dns_client_socket.sendto(dns_lockon.encode(), destination_address)
    
    domain = input("Enter domain to remove: ")
    record_data = f"remove,{domain}"
    dns_client_socket.sendto(record_data.encode(), destination_address)

    response, _ = dns_client_socket.recvfrom(1024)
    print(response.decode())

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
                add_records(client_socket, server_address)
            case "/remove":
                remove_records(client_socket, server_address)
            case "/exit":
                print("Please Confirm...")
                choice = "n"

        choice = input("Do you want to continue? (y/n): ")
        if choice.lower() != 'y':
            serverTermination = "quit"
            client_socket.sendto(serverTermination.encode(), server_address)
            break
    
    client_socket.close()

main()
print("Thank you for using this network application\n")
print("Created by Venujan Malaiyandi")


                