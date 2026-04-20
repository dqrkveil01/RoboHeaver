#!/bin/bash

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}===========================================${NC}"
echo -e "${YELLOW}       Instalador do DataStalker        ${NC}"
echo -e "${CYAN}===========================================${NC}"

echo -e "\n${YELLOW}[*] Atualizando pacotes do Termux...${NC}"
pkg update -y > /dev/null 2>&1
pkg upgrade -y > /dev/null 2>&1
echo -e "${GREEN}[+] Pacotes atualizados.${NC}"

echo -e "\n${YELLOW}[*] Instalando dependências (Python, Git, Curl)...${NC}"
pkg install -y python git curl > /dev/null 2>&1
echo -e "${GREEN}[+] Dependências instaladas.${NC}"

echo -e "\n${YELLOW}[*] Instalando bibliotecas Python...${NC}"
pip install requests beautifulsoup4 > /dev/null 2>&1
echo -e "${GREEN}[+] Bibliotecas Python instaladas.${NC}"

echo -e "\n${YELLOW}[*] Dando permissão de execução à ferramenta...${NC}"
chmod +x stalker.py

echo -e "\n${GREEN}===========================================${NC}"
echo -e "${GREEN}   INSTALAÇÃO CONCLUÍDA COM SUCESSO!   "
echo -e "\n   Para iniciar, use o comando: python stalker.py"
echo -e "${GREEN}===========================================${NC}"
