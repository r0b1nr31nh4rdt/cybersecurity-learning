import socket

def build_dns_query(domain: str) -> bytes:
    # Header
    transaction_id = b'\xAB\xCD'   # 2-Byte-ID
    flags         = b'\x01\x00'    # Standard-Query, Recursion desired
    qdcount       = b'\x00\x01'    # 1 question
    ancount       = b'\x00\x00'
    nscount       = b'\x00\x00'
    arcount       = b'\x00\x00'
    header = transaction_id + flags + qdcount + ancount + nscount + arcount

    # Question Section – Domain encoding
    qname = b''
    for part in domain.split('.'):
        encoded = part.encode()
        qname += bytes([len(encoded)]) + encoded
    qname += b'\x00'  # Root-Label

    qtype  = b'\x00\x01'  # A-Record
    qclass = b'\x00\x01'  # IN (Internet)

    return header + qname + qtype + qclass



def dns_crafter():

    payload = build_dns_query("example.com")
    print(payload.hex())

    # create UDP socket
    sock = socket.socket(
        socket.AF_INET,   # IPv4
        socket.SOCK_DGRAM # UDP (instead SOCK_STREAM for TCP)
    )
    sock.settimeout(2)


    try:
        # send DNS query
        dns_server = ("8.8.8.8", 53)
        sock.sendto(payload, dns_server)

        # receive response
        response, _ = sock.recvfrom(512)  # 512 Bytes = Standard DNS-buffer-size
        print(response.hex())

    except socket.error as err:
        print(f"Client: Socket error: {err}")
    except KeyboardInterrupt:
        print("\nClient: Disconnecting...")
    finally:
        sock.close()


if __name__ == "__main__":

    dns_crafter()