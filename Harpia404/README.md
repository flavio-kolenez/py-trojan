# Python Reverse Shell - Projeto Educacional

> ⚠️ **AVISO**: Este projeto é destinado exclusivamente para fins educacionais e de pesquisa em segurança cibernética. Use apenas em ambientes controlados com autorização explícita.

## 📚 Recursos de Estudo

### Livros Recomendados
- "Black Hat Python" - Justin Seitz
- "Gray Hat Hacking" - Shon Harris
- "The Hacker Playbook 3" - Peter Kim

### Plataformas de Prática
- **HackTheBox** - Laboratórios de pentest
- **TryHackMe** - Exercícios guiados
- **VulnHub** - VMs vulneráveis
- **OverTheWire** - Wargames

### Tools Relacionadas
- **Metasploit** - Framework de exploit
- **Cobalt Strike** - Red team operations
- **Empire** - PowerShell post-exploitation
- **Ncat/Netcat** - Network communication

## 📟 Sistema de Logging

O projeto utiliza ícones padronizados para categorizar as mensagens de output:

| Ícone | Categoria | Descrição |
|-------|-----------|-----------|
| `[!]` | **Erros** | Falhas de cópia, conexão, comandos, etc. |
| `[+]` | **Sucesso** | Operações completadas com sucesso |
| `[*]` | **Informação** | Status geral, inicialização do sistema |
| `[~]` | **Retry/Reconexão** | Tentativas de reconexão automática |
| `[>]` | **Output** | Resultado de comandos executados |
| `[^]` | **Interrupção** | Parada manual pelo usuário |

### Exemplo de Output
```
[*] Starting client, connecting to 192.168.1.78:443
[+] Connected successfully!
[>] Command executed successfully
[~] Connection closed, retrying...
[!] Connection Error: [Errno 10061] No connection could be made
[^] Program interrupted by user
```

## ⚠️ Disclaimer Legal

Este software é fornecido para fins educacionais e de pesquisa apenas. O uso deste código para:

- Acessar sistemas sem autorização
- Prejudicar infraestrutura de TI
- Violar leis de privacidade e segurança
- Qualquer atividade ilegal

É **ESTRITAMENTE PROIBIDO** e pode resultar em consequências legais graves.

**Use com responsabilidade e apenas em ambientes autorizados.**

---

## 📝 Licença

Este projeto é disponibilizado para fins educacionais. O desenvolvedor não se responsabiliza pelo uso inadequado desta ferramenta.

**Developed for Educational Purposes - Red Team Training**