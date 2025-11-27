# NetManager - Cisco Network Automation

> **Projeto Final - Cisco DevNet Associate (DevAsc)**
> Uma plataforma Full-Stack para gestão de infraestrutura de rede, abstraindo a complexidade do CLI através de uma interface Web moderna.


## Sobre o Projeto

O **NetManager** foi desenvolvido como projeto de conclusão do curso de 3 meses da **Cisco Networking Academy (DevNet)**. O objetivo principal é resolver a ineficiência e o risco de erro humano associados à configuração manual de switches via CLI.

A aplicação permite que operadores de rede (NOC/N1) visualizem, criem e modifiquem VLANs e atribuam portas, tudo através de um Dashboard intuitivo, sem precisarem de tocar num terminal SSH.


## Tech Stack

### Back-end
*   **Python 3:** Linguagem base.
*   **FastAPI:** Framework web de alta performance para a API e rotas.
*   **Uvicorn:** Servidor ASGI.
*   **Requests:** Para comunicação via API RESTCONF (IOS XE).
*   **Netmiko:** (Suporte legado) Para automação via SSH.

### Front-end
*   **HTML5 / Jinja2:** Templates dinâmicos.
*   **Tailwind CSS:** Estilização moderna e responsiva.
*   **Vis.js:** Biblioteca para renderização de grafos e topologias de rede.
*   **FontAwesome:** Ícones.

## Como Rodar o Projeto

### Pré-requisitos
*   Python 3.8 ou superior instalado.

### 1. Clonar o Repositório
```bash
git clone https://github.com/SEU-USUARIO/NetManager.git
cd NetManager

# 2. Criar Ambiente Virtual e Instalar Dependências

# Windows
python -m venv AmbienteVirtual
.\AmbienteVirtual\Scripts\activate

# Linux/Mac
python3 -m venv AmbienteVirtual
source AmbienteVirtual/bin/activate

# Instalar bibliotecas
pip install -r requirements.txt

# 3 Executar (Modo Simulação)
Este projeto inclui um Mock Router para testar todas as funcionalidades localmente. Precisará de dois terminais abertos:
Terminal 1 (Simulador do Router):
    python mock_router.py
    # Roda na porta 8888
Terminal 2 (Aplicação Web):
uvicorn main:app --reload --port 8000
#4. Acessar
Abra o navegador em: http://127.0.0.1:8000
---------------------------------------------------------------------------------
⚙️ Configuração (Real vs Mock)
O comportamento da aplicação é controlado pelo arquivo config.py.
Para usar o Simulador Local:
USE_MOCK = False
SANDBOX = { "host": "127.0.0.1", "port": 8888, ... }
# Nota: O código atual conecta via HTTP ao mock_router.py
Para conectar a um Cisco Sandbox (DevNet):
Reserve um laboratório "IOS XE on Catalyst 8000v" no Cisco DevNet.
Conecte a VPN (Cisco AnyConnect).
Atualize o config.py com o IP e Credenciais do Lab.
 
 # Screenshots
screenshots/dashboard.png
screenshots/topologia.png

🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir Issues ou enviar Pull Requests.

Desenvolvido por Manuel de Deus
Cisco Certified DevNet Associate Candidate