# RoboReaver 🤖

RoboReaver é uma ferramenta de ataque de força bruta para o Roblox, construída com uma interface de linha de comando (CLI) impressionante e funcionalidades avançadas. Projetada para pesquisa de segurança e testes de penetração em ambientes autorizados, ela utiliza multi-threading para testar milhares de senhas em minutos.

## ✨ Funcionalidades Incríveis

- **Interface Profissional**: Menus coloridos, banners e uma barra de progresso em tempo real que mostra o ataque acontecendo.
- **Ataque Multi-Thread**: Use múltiplas threads para acelerar drasticamente o processo de brute-force.
- **Simulação Inteligente**: A ferramenta simula um navegador real, obtendo tokens `X-CSRF` necessários para enganar as defesas básicas do Roblox.
- **Detecção de Bloqueio**: Pausa automaticamente o ataque se detectar que o Roblox está bloqueando as tentativas (Rate Limit).
- **Relatório Claro**: Exibe uma mensagem de sucesso gigante se a senha for encontrada ou informa claramente se a busca falhou.
- **Fácil de Usar**: Guiado por menus interativos.

## 🚀 Instalação (Termux)

A instalação é super simples e automatizada.

```bash
# 1. Atualize o Termux e instale o Git
pkg update -y && pkg upgrade -y
pkg install git -y

# 2. Clone o repositório do RoboReaver
# !! TROQUE 'SEU-USUARIO' E 'SEU-REPOSITORIO' PELO LINK REAL !!
git clone https://github.com/dqrkveil01/RoboHeaver/

# 3. Entre no diretório da ferramenta
cd RoboHeaver

# 4. Execute o script de instalação
bash install.sh
```

## ⚙️ Como Usar

### 1. Prepare sua Wordlist

A força bruta depende de uma boa lista de senhas (`wordlist`). Crie um arquivo chamado `wordlist.txt` (ou qualquer outro nome) e coloque uma senha por linha.

```
senha1
123456
nomedocachorro
...
```

### 2. Inicie a Ferramenta

No mesmo diretório onde você clonou o projeto, execute:

```bash
python reaver.py
```

### 3. Siga as Instruções

O menu principal aparecerá:

- Escolha **`[1] Iniciar Ataque Brute-Force`**.
- Digite o **username** do alvo no Roblox.
- Forneça o **caminho para o seu arquivo de wordlist** (ex: `wordlist.txt`).
- Escolha o **número de threads** (comece com um número baixo como 10 para evitar bloqueios).
- Sente-se e observe o ataque acontecer em tempo real.
