#!/bin/bash
# Configurações de rede do Kali
# 1. Limpa qualquer IP anterior na eth0 para não dar conflito
sudo ip addr flush dev eth0

# 2. Adiciona o seu IP do Kali (100.20)
sudo ip addr add 192.168.100.20/24 dev eth0

# 3. Garante que a interface esteja ligada (UP)
sudo ip link set eth0 up

# 4. (Opcional) Adiciona uma rota padrão se precisar, mas o /24 já resolve o local
# sudo ip route add 192.168.100.0/24 dev eth0

echo "[!] Rede configurada!"
echo "[.] IP atual do Kali:"
ip addr show eth0 | grep "inet "
echo "[.] Tentando pingar o BWA (192.168.100.10)..."
ping -c 3 192.168.100.10
                          