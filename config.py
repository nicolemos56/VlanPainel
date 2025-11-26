# config.py

USE_MOCK = False 

# Configuração para o Router Falso Local
SANDBOX = {
    "host": "127.0.0.1",
    "port": 8888,         # Porta do mock_router.py
    "username": "admin",  # Não importa, o mock aceita qualquer coisa
    "password": "admin"
}

HEADERS = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}

import urllib3
urllib3.disable_warnings()