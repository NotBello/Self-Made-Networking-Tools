import socket
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

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', 53))
    print("DNS server is running.")

    while True:
        client_option, client_address = server_socket.recvfrom(1024)
        formated_client_option = client_option.decode()
        match formated_client_option:
            case "dnslookup":
                query, _ = server_socket.recvfrom(1024)
                response = handler(query)
                server_socket.sendto(response, client_address)
            case "dnslist":
                table_data = []
                for domain, record in dns_records.items():
                    table_data.append([domain, record['type'], record['value']])

                headers = ['Domain', 'Type', 'Value']
                table = tabulate(table_data, headers, tablefmt='grid')

                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                sock.sendto(table.encode(), client_address)
                

if __name__ == "__main__":
    main()
