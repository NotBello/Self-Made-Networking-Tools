import socket

# DNS records (for simplicity, hardcoded)
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
        query, client_address = server_socket.recvfrom(1024)
        response = handler(query)
        server_socket.sendto(response, client_address)

if __name__ == "__main__":
    main()
