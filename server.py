import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button
from DES import DES

KEY = 'secret_k'


def handle_client(client_socket):
    while True:
        global KEY
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break
            d = DES(KEY)
            # Update the UI with the received message
            server_display.insert(tk.END, f"Client: {d.decrypt(data.decode('utf-8'))}\n")
            server_display.yview(tk.END)
        except:
            break

    client_socket.close()


def send_message():
    global KEY
    # Get the message from the entry widget
    message = server_entry.get()
    d = DES(KEY)
    # Send the message to the client
    client_socket.send(d.encrypt(message).encode('utf-8'))

    # Update the server UI with the sent message
    server_display.insert(tk.END, f"Server: {message}\n")
    server_display.yview(tk.END)

    # Clear the entry widget after sending the message
    server_entry.delete(0, tk.END)


# Set up the server UI
server = tk.Tk()
server.title("Chat Server")

server_display = scrolledtext.ScrolledText(server, width=40, height=10)
server_display.pack(padx=10, pady=10)

server_entry = Entry(server, width=30)
server_entry.pack(padx=10, pady=10)

send_button = Button(server, text="Send", command=send_message)
send_button.pack(padx=10, pady=10)

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5555))
print(socket.gethostbyname(socket.gethostname()))
server_socket.listen(1)

print("[*] Server listening on port 5555")

# Accept a connection from a client
client_socket, addr = server_socket.accept()
print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

# Create a thread to handle the client
client_handler = threading.Thread(target=handle_client, args=(client_socket,))
client_handler.start()

# Start the Tkinter main loop
server.mainloop()
