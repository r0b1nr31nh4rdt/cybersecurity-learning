import socket

"""
A netcat "server" will send a message in chunks. Start it with: { echo -n 'The journey of a thousand miles '; sleep 0.5; echo -n 'begins with a single '; sleep 0.5; echo -n 'SYN packet. FORTUNE: '; sleep 0.5; echo -n 'Embrace the ACK!'; sleep 0.5; echo ' The rest is just data.'; } | nc -l 44556 .
"""

def fortune_client():

    client_socket = socket.socket()
    try:
        server_address = ("127.0.0.1", 44556)
        client_socket.connect(server_address)
        print("client connected")

        mystring = ""

        while True:
            data_received = client_socket.recv(1024)
            if not data_received:
                break
            mystring += data_received.decode('utf-8')
            print(f"Client: Message received: {data_received.decode('utf-8')}")
            print(f"mystring: {mystring}")
        print("Client: Connection closed by server")
        splitstring = mystring.split("FORTUNE: ")
        print(f"The fortune is: {splitstring[1]}")


    except socket.error as err:
        print(f"Client: Socket error: {err}")
    except KeyboardInterrupt:
        print("\nClient: Disconnecting...")
    finally:
        client_socket.close()


if __name__ == "__main__":
    fortune_client()
