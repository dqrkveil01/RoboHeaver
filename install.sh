#!/bin/bash
# RoboReaver v3 - Instalador Detalhado

# --- CORES ---
C='\033[0;36m' # Cyan
Y='\033[1;33m' # Yellow
G='\033[0;32m' # Green
R='\033[0;31m' # Red
NC='\033[0m'   # No Color

clear
echo -e "${R}=====================================================${NC}"
echo -e "${Y}      INSTALADOR DO ROBOREAVER v3: ANNIHILATOR       ${NC}"
echo -e "${R}=====================================================${NC}"
echo ""
echo -e "${C}[ETAPA 1/4]${NC} Atualizando os repositórios do Termux..."
echo -e "${Y}Isso pode demorar um pouco, por favor, aguarde...${NC}"
pkg update -y
echo -e "${G}[SUCESSO]${NC} Repositórios atualizados."
echo ""

echo -e "${C}[ETAPA 2/4]${NC} Instalando pacotes essenciais (git, python)..."
pkg install -y git python
echo -e "${G}[SUCESSO]${NC} Pacotes essenciais instalados."
echo ""

echo -e "${C}[ETAPA 3/4]${NC} Criando diretórios para logs e checkpoints..."
mkdir -p logs
mkdir -p checkpoints
echo -e "${G}[SUCESSO]${NC} Diretórios criados."
echo ""

echo -e "${C}[ETAPA 4/4]${NC} Dando permissão de execução à ferramenta principal..."
chmod +x reaver.py
echo -e "${G}[SUCESSO]${NC} Permissão concedida."
echo ""

echo -e "${G}=====================================================${NC}"
echo -e "${G}   TUDO PRONTO! A MÁQUINA DE GUERRA ESTÁ MONTADA.    ${NC}"
echo -e "${G}=====================================================${NC}"
echo -e "\nO script principal instalará as bibliotecas Python na primeira execução."
echo -e "Para iniciar o massacre, use: ${Y}python reaver.py${NC}"
echo ""
