import socket as s
import threading as th
import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None

option = input("Select (1) for hosting or Select (2) to connect: ")

if option == "1":
    server = s.socket(s.AF_INET, s.SOCK_STREAM)
    server.bind(("172.20.10.5", 32421))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
elif option == "2":
    client = s.socket(s.AF_INET, s.SOCK_STREAM)
    client.connect(("172.20.10.5", 32421))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
else:
    print("Your input option is wrong")
    exit()

def sending_messages(c):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)

def receiving_messages(c):
    while True:
        print("Other User: " + rsa.decrypt(c.recv(1024), private_key).decode())

th.Thread(target=sending_messages, args=(client,)).start()
th.Thread(target=receiving_messages, args=(client,)).start()