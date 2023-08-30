import socket
import sys
from tabulate import tabulate

dns_records = {
    'www.google.com': {'type': 'A', 'value': '172.255.31.1'},
    'mail.example.com': {'type': 'A', 'value': '222.168.117.8'},
    'alias.example.com': {'type': 'CNAME', 'value': 'www.example.com'},
}

def handler(query):
    hostname = query.decode()
    
    if hostname in dns_records:
        record = dns_records[hostname]
        response = f"{hostname} {record['type']} {record['value']}"
    else:
        response = "Not found"

    return response.encode()

def dns_lookup(dns_server_socket, dns_client_address):
    query, _ = dns_server_socket.recvfrom(1024)
    response = handler(query)
    dns_server_socket.sendto(response, dns_client_address)

def dns_listall():
    table_data = []
    for domain, record in dns_records.items():
        table_data.append([domain, record['type'], record['value']])

    headers = ['Domain', 'Type', 'Value']
    tabular = tabulate(table_data, headers, tablefmt='grid')
    return tabular

def dns_add(dns_server_socket, dns_client_address):
    data, addr = dns_server_socket.recvfrom(1024)
    received_record = data.decode()

    # Assuming the received record is in the format: 'domain,type,value'
    domain, record_type, value = received_record.split(',')

    dns_records[domain] = {'type': record_type, 'value': value}

    response = dns_listall()
    dns_server_socket.sendto(response.encode(), addr)

def dns_rem(dns_server_socket, dns_client_address):
    data, addr = dns_server_socket.recvfrom(1024)
    received_data = data.decode()

    # Assuming the received data is in the format: 'action,domain'
    action, domain = received_data.split(',')

    if action == 'remove':
        if domain in dns_records:
            del dns_records[domain]
            response = f"Record for '{domain}' removed."
        else:
            response = f"No record found for '{domain}'."

    elif action == 'display':
        response = dns_listall()

    dns_server_socket.sendto(response.encode(), addr)


def dns_main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', 53))
    print("DNS server is running.")

    while True:
        client_option, client_address = server_socket.recvfrom(1024)
        formated_client_option = client_option.decode()
        match formated_client_option:
            case "dnslookup":
                dns_lookup(server_socket, client_address)
            case "dnslist":
                table = dns_listall()
                server_socket.sendto(table.encode(), client_address)
            case "dnsadd":
                dns_add(server_socket, client_address)
            case "dnsremove":
                dns_rem(server_socket, client_address)

        
        print("Termination")
        serverdata, addr = server_socket.recvfrom(1024)
        termination = serverdata.decode()

        if termination.lower() == "quit":
            break

    server_socket.close()
    print("FTermination")



dns_main()
sys.exit(0)