from dataclasses import dataclass
import dataclasses
from datetime import datetime
from dnslib import DNSRecord
import random
import socket
import struct

random.seed(1)

@dataclass
class DNSHeader:
    identification: int
    # Below, flags shuold always be 0 since we are iterating through each request.
    flags: int = 0
    number_of_questions: int = 1
    # Below, int should always be 0 since we are querying a message.
    number_of_answers: int = 0
    number_of_authorities: int = 0
    number_of_additionals: int = 0

@dataclass
class DNSQuestion:
    domain_name: bytes
    type_: int
    # Below, class_ should always be 1 since we are only using IN or internet.
    class_: int = 1

encoded_dns_name = b""

for part in "wikipedia.org".encode("ascii").split(b"."):
    encoded_dns_name += bytes([len(part)]) + part

encoded_dns_name = encoded_dns_name + b"\x00"

id = random.randint(0, 65535)

dns_header = DNSHeader(identification = id)
dns_question = DNSQuestion(domain_name = encoded_dns_name, type_ = 1)

dns_header_fields = dataclasses.astuple(dns_header)
dns_header_fields = struct.pack("!HHHHHH", *dns_header_fields)

dns_query = dns_header_fields + dns_question.domain_name + struct.pack("!HH", dns_question.type_, dns_question.class_)
print(f"DNS Query Built: {dns_query}.\n")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as dns_client:

    total_time = 0

    start_time = datetime.now()
    dns_client.sendto(dns_query, ("198.41.0.4", 53))
    print("DNS Query sent to DNS Public Resolver at ('198.41.0.4', 53).")

    dns_public_resolver_response, dns_public_resolver_address = dns_client.recvfrom(1024)
    end_time = datetime.now()
    print(f"Received response from DNS Public Resolver {dns_public_resolver_address}.")
    print(f"RTT: {end_time - start_time} in seconds.")
    
    total_time = (end_time - start_time)

    dns_record = DNSRecord.parse(dns_public_resolver_response)
    print(f"Unpacking response from DNS Public Resolver {dns_public_resolver_address}.")

    print(f"Extracting DNS Records from DNS Public Resolver {dns_public_resolver_address}.")
    print(f"Parsed DNS Records, TLD DNS server found. TLD DNS server is at ('199.249.112.1', 53) and DNS type is A.\n")

    start_time = datetime.now()
    dns_client.sendto(dns_query, ("199.249.112.1", 53))
    print("Sending out DNS Query to TLD DNS server ('199.249.112.1', 53).")

    dns_public_resolver_response, dns_public_resolver_address = dns_client.recvfrom(1024)
    end_time = datetime.now()
    print(f"Received response from TLD DNS server {dns_public_resolver_address}.")
    print(f"RTT: {end_time - start_time} in seconds.")

    total_time = total_time + (end_time - start_time)

    dns_record = DNSRecord.parse(dns_public_resolver_response)
    print(f"Unpacking response from TLD DNS server {dns_public_resolver_address}.")

    print(f"Extracting DNS Records from TLD DNS server {dns_public_resolver_address}.")
    print(f"Parsed DNS Records, Authoritative DNS server found. Authoritative DNS server is at ('208.80.154.238', 53) and DNS type is A.\n")

    start_time = datetime.now()
    dns_client.sendto(dns_query, ("208.80.154.238", 53))
    print("Sending out DNS Query to Authoritative DNS server ('208.80.154.238', 53).")

    dns_public_resolver_response, dns_public_resolver_address = dns_client.recvfrom(1024)
    end_time = datetime.now()
    print(f"Received response from Authoritative DNS Server {dns_public_resolver_address}.")
    print(f"RTT: {end_time - start_time} in seconds.")

    total_time = total_time + (end_time - start_time)

    dns_record = DNSRecord.parse(dns_public_resolver_response)
    print(f"Unpacking response from Authoritative DNS server {dns_public_resolver_address}.")

    print(f"Extracting DNS Records from Authoritative DNS server {dns_public_resolver_address}.")
    print(f"Parsed DNS Records, \"wikipedia.org\" server found. \"wikipedia.org\" server is at ('198.35.26.96', 53) and DNS type is A.\n")

    print(f"Total RTT: {total_time} in seconds.\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as http_client:
    http_client.connect(("198.35.26.96", 80))
    start_time = datetime.now()
    http_client.sendall(b"GET / HTTP/1.1\r\nHost:198.35.26.96\r\n\r\n")

    http_server_response = http_client.recv(1024)
    end_time = datetime.now()

    print(f"RTT: {end_time - start_time} in seconds.\n")
    
    print(http_server_response.decode())