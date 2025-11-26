# vlan_manager.py
import requests
import json
import os
from requests.auth import HTTPBasicAuth
from config import SANDBOX, HEADERS, USE_MOCK

# --- MOCK (Simulação Local) ---
MOCK_FILE = "mock_vlans.json"

def _load_mock():
    if not os.path.exists(MOCK_FILE): return []
    with open(MOCK_FILE, 'r') as f: return json.load(f)

def _save_mock(data):
    with open(MOCK_FILE, 'w') as f: json.dump(data, f)

# --- FUNÇÕES REAIS (RESTCONF) ---

def get_vlans():
    if USE_MOCK: return _load_mock()

    url = f"http://{SANDBOX['host']}:{SANDBOX['port']}/restconf/data/Cisco-IOS-XE-native:native/vlan"
    auth = HTTPBasicAuth(SANDBOX['username'], SANDBOX['password'])

    try:
        print(f"Conectando a {SANDBOX['host']}...")
        response = requests.get(url, headers=HEADERS, auth=auth, verify=False, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        # Caminho no JSON do IOS XE
        vlans_raw = data.get("Cisco-IOS-XE-native:vlan", {}).get("vlan-list", [])
        return vlans_raw

    except Exception as e:
        print(f"Erro na API: {e}")
        return []

def create_vlan(vlan_id, vlan_name):
    if USE_MOCK:
        vlans = _load_mock()
        vlans.append({"id": int(vlan_id), "name": vlan_name})
        _save_mock(vlans)
        return True, "Criado no Mock"

    url = f"http://{SANDBOX['host']}:{SANDBOX['port']}/restconf/data/Cisco-IOS-XE-native:native/vlan"
    auth = HTTPBasicAuth(SANDBOX['username'], SANDBOX['password'])
    
    # Formato YANG para criar VLAN
    payload = {
        "Cisco-IOS-XE-native:vlan-list": [
            {
                "id": int(vlan_id),
                "name": vlan_name
            }
        ]
    }

    try:
        response = requests.patch(url, headers=HEADERS, auth=auth, json=payload, verify=False, timeout=10)
        if response.status_code in [200, 204]:
            return True, "Sucesso"
        return False, response.text
    except Exception as e:
        return False, str(e)

def delete_vlan(vlan_id):
    if USE_MOCK:
        vlans = _load_mock()
        novas = [v for v in vlans if v['id'] != int(vlan_id)]
        _save_mock(novas)
        return True, "Apagado no Mock"

    # URL específica para o ID da VLAN
    url = f"http://{SANDBOX['host']}:{SANDBOX['port']}/restconf/data/Cisco-IOS-XE-native:native/vlan/vlan-list={vlan_id}"
    auth = HTTPBasicAuth(SANDBOX['username'], SANDBOX['password'])

    try:
        response = requests.delete(url, headers=HEADERS, auth=auth, verify=False, timeout=10)
        if response.status_code in [200, 204]:
            return True, "Sucesso"
        return False, response.text
    except Exception as e:
        return False, str(e)
    # Adicionar no final de vlan_manager.py

def get_interfaces():
    """Busca a lista de interfaces e suas VLANs atuais"""
    url = f"http://{SANDBOX['host']}:{SANDBOX['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"
    try:
        response = requests.get(url, headers=HEADERS, auth=HTTPBasicAuth(SANDBOX['username'], SANDBOX['password']), timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("Cisco-IOS-XE-native:GigabitEthernet", [])
    except Exception as e:
        print(f"Erro ao ler interfaces: {e}")
        return []

def assign_vlan(interface_name, vlan_id):
    """Atribui uma VLAN a uma porta específica (switchport access vlan X)"""
    # URL específica para editar UMA interface
    url = f"http://{SANDBOX['host']}:{SANDBOX['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet={interface_name}"
    
    # Payload equivalente a: interface GiX -> switchport access vlan Y
    payload = {
        "Cisco-IOS-XE-native:GigabitEthernet": {
            "name": interface_name,
            "switchport": {
                "access": {
                    "vlan": int(vlan_id)
                }
            }
        }
    }

    try:
        response = requests.patch(url, headers=HEADERS, auth=HTTPBasicAuth(SANDBOX['username'], SANDBOX['password']), json=payload, timeout=5)
        if response.status_code in [200, 204]:
            return True, "Porta configurada com sucesso"
        return False, response.text
    except Exception as e:
        return False, str(e)