# Guia de Configuração do Laboratório

Este documento orienta a configuração de rede para o ambiente de laboratório, utilizando Kali Linux e o servidor BWA.

## Passo a passo no Kali Linux

Execute o script de configuração:

```
./config_lab.sh
```

Esse script automatiza a preparação do ambiente, ajustando interfaces e rotas conforme necessário. Certifique-se de dar permissão de execução ao script, caso necessário:

```
sudo chmod +x config_lab.sh
```

## Configuração manual no servidor BWA

É possivel criar um script para automatizar o processo utilizando `nano connect_bwa_network.sh` e colando dentro dele os comandos seguintes: 

```
sudo ip addr flush dev eth0
sudo ip addr add 192.168.100.10/24 dev eth0
sudo ip link set eth0 up
```

Salve (Ctrl+O, Enter, Ctrl+X) e dê permissão: chmod +x ligar_rede.sh

Esses comandos garantem que a interface eth0 esteja com o IP correto e ativa para comunicação com o Kali.

## Testando a conexão

Dentro do Kali: `ping 192.168.100.10` isso vai tentar pingar a BWA. Se não funcionar, siga para o próximo tópico: [Dicas e possíveis problemas](#dicas-e-possiveis-problemas)

## Dicas e possíveis problemas

- Verifique se o cabo de rede está conectado corretamente.
- Use `ip a` para conferir se o IP foi aplicado.
- Se houver conflitos de IP, ajuste o endereço conforme a topologia do laboratório.
- Para persistência após reboot, edite o arquivo de configuração de rede do sistema (ex: `/etc/network/interfaces` ou scripts de inicialização).
- O script `config_lab.sh` pode ser adaptado para outros cenários, basta alterar os parâmetros de rede.

## Referências úteis
- [Documentação oficial iproute2](https://www.man7.org/linux/man-pages/man8/ip.8.html)
- [Configuração de rede no Kali Linux](https://www.kali.org/docs/networking/)

---