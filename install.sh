#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'
echo -e "${CYAN}===========================================${NC}"
echo -e "${YELLOW}         Instalador do RoboReaver v2        ${NC}"
echo -e "${CYAN}===========================================${NC}"
echo -e "\n${YELLOW}[*] Atualizando pacotes e instalando Git...${NC}"
pkg update -y > /dev/null 2>&1
pkg install -y git python > /dev/null 2>&1
echo -e "${GREEN}[+] Ambiente básico preparado.${NC}"
echo -e "\n${YELLOW}[*] Dando permissão de execução à ferramenta...${NC}"
chmod +x reaver.py
echo -e "\n${GREEN}===========================================${NC}"
echo -e "${GREEN}      INSTALAÇÃO CONCLUÍDA COM SUCESSO!   "
echo -e "\n   O script principal instalará as dependências Python."
echo -e "   Para iniciar, use: ${CYAN}python reaver.py${NC}"
echo -e "${GREEN}===========================================${NC}"
