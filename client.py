import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button
from DES import DES

KEY = 'secret_k'

def receive():
    while True:
        global KEY
        try:
            # Receive data from the server
            data = client_socket.recv(1024)
            if not data:
                break
            d = DES(KEY)
            # Update the UI with the received message
            client_display.insert(tk.END, f"Server: {d.decrypt(data.decode('utf-8'))}\n")
            client_display.yview(tk.END)
        except:
            break


def send_message():
    global KEY
    # Get the message from the entry widget
    message = client_entry.get()

    d = DES(KEY)
    # Send the message to the server
    client_socket.send(d.encrypt(message).encode('utf-8'))

    # Update the client UI with the sent message
    client_display.insert(tk.END, f"Client: {message}\n")
    client_display.yview(tk.END)

    # Clear the entry widget after sending the message
    client_entry.delete(0, tk.END)


# Function to connect to the server with the provided IP address
def connect_to_server():
    global client_socket
    server_ip = server_entry.get()

    try:
        # Set up the client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, 5555))

        # Create a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        # Enable the message entry and send button
        client_entry.config(state=tk.NORMAL)
        send_button.config(state=tk.NORMAL)

        # Disable the connect button
        connect_button.config(state=tk.DISABLED)
    except Exception as e:
        client_display.insert(tk.END, f"Error connecting to the server: {str(e)}\n")
        client_display.yview(tk.END)


# Set up the client UI
client = tk.Tk()
client.title("Chat Client")

client_display = scrolledtext.ScrolledText(client, width=40, height=10)
client_display.pack(padx=10, pady=10)

server_entry = Entry(client, width=30)
server_entry.pack(padx=10, pady=10)

connect_button = Button(client, text="Connect", command=connect_to_server)
connect_button.pack(padx=10, pady=10)

client_entry = Entry(client, width=30, state=tk.DISABLED)
client_entry.pack(padx=10, pady=10)

send_button = Button(client, text="Send", command=send_message, state=tk.DISABLED)
send_button.pack(padx=10, pady=10)

# Start the Tkinter main loop
client.mainloop()
