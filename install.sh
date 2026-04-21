#!/bin/bash
# RoboReaver v4 - Instalador Transparente

# --- CORES ---
C='\033[0;36m' # Cyan
Y='\033[1;33m' # Yellow
G='\033[0;32m' # Green
R='\033[0;31m' # Red
NC='\033[0m'   # No Color

clear
echo -e "${R}=====================================================${NC}"
echo -e "${Y}         ROBOREAVER v4: THE COLOSSUS - SETUP         ${NC}"
echo -e "${R}=====================================================${NC}"
echo ""

# ETAPA 1
echo -e "${C}[ETAPA 1/3]${NC} Atualizando repositórios do Termux..."
echo -e "${Y}--- SAÍDA DO COMANDO ABAIXO ---${NC}"
pkg update -y
echo -e "${Y}-------------------------------${NC}"
echo -e "${G}[SUCESSO]${NC} Repositórios atualizados."
echo ""
sleep 1

# ETAPA 2
echo -e "${C}[ETAPA 2/3]${NC} Instalando pacotes essenciais (git, python)..."
echo -e "${Y}--- SAÍDA DO COMANDO ABAIXO ---${NC}"
pkg install -y git python
echo -e "${Y}-------------------------------${NC}"
echo -e "${G}[SUCESSO]${NC} Pacotes essenciais instalados."
echo ""
sleep 1

# ETAPA 3
echo -e "${C}[ETAPA 3/3]${NC} Dando permissão de execução ao Colossus..."
chmod +x reaver.py
echo -e "${G}[SUCESSO]${NC} Permissão de aniquilação concedida."
echo ""
sleep 1

# FINALIZAÇÃO
echo -e "${R}=====================================================${NC}"
echo -e "${G}     O COLOSSUS ESTÁ PRONTO PARA A BATALHA.          ${NC}"
echo -e "${R}=====================================================${NC}"
echo -e "\nO script principal instalará as bibliotecas Python necessárias."
echo -e "Para iniciar, use: ${Y}python reaver.py${NC}"
echo ""
echo -e "${G}=====================================================${NC}"
echo -e "${G}   TUDO PRONTO! A MÁQUINA DE GUERRA ESTÁ MONTADA.    ${NC}"
echo -e "${G}=====================================================${NC}"
echo -e "\nO script principal instalará as bibliotecas Python na primeira execução."
echo -e "Para iniciar o massacre, use: ${Y}python reaver.py${NC}"
echo ""
