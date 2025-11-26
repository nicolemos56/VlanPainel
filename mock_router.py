# mock_router.py
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Simulador Cisco IOS XE")

# --- BASE DE DADOS EM MEMÓRIA ---
# VLANs
vlans_db = [
    {"id": 1, "name": "default"},
    {"id": 10, "name": "Vendas"},
    {"id": 20, "name": "TI"}
]

# Interfaces (Portas) - Começam todas na VLAN 1
# No mock_router.py, substitui a lista interfaces_db por esta:

interfaces_db = [
    {"name": "1", "description": "PC3", "vlan": 10},
    {"name": "2", "description": "PC4", "vlan": 10},
    {"name": "3", "description": "PC5", "vlan": 20},
    {"name": "4", "description": "PC6", "vlan": 20},
    {"name": "5", "description": "Router1_Gateway", "vlan": 1},
    {"name": "6", "description": "Livre", "vlan": 1}
]

# --- ENDPOINTS VLAN (JÁ EXISTIAM) ---
@app.get("/restconf/data/Cisco-IOS-XE-native:native/vlan")
async def get_vlans():
    return {"Cisco-IOS-XE-native:vlan": {"vlan-list": vlans_db}}

@app.patch("/restconf/data/Cisco-IOS-XE-native:native/vlan")
async def create_vlan(request: Request):
    body = await request.json()
    items = body.get("Cisco-IOS-XE-native:vlan-list", [])
    for item in items:
        v_id = item.get("id")
        v_name = item.get("name")
        print(f"📡 VLAN: Criando/Atualizando VLAN {v_id} ({v_name})")
        existing = next((v for v in vlans_db if v["id"] == v_id), None)
        if existing: existing["name"] = v_name
        else: vlans_db.append({"id": v_id, "name": v_name})
    return Response(status_code=204)

@app.delete("/restconf/data/Cisco-IOS-XE-native:native/vlan/vlan-list={vlan_id}")
async def delete_vlan(vlan_id: int):
    print(f"📡 VLAN: Apagando VLAN {vlan_id}")
    global vlans_db
    vlans_db = [v for v in vlans_db if v["id"] != vlan_id]
    return Response(status_code=204)

# --- NOVOS ENDPOINTS: INTERFACES (PORTAS) ---

# 1. GET - Listar Interfaces
@app.get("/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet")
async def get_interfaces():
    # Estrutura complexa do IOS XE simplificada para o mock
    lista_formatada = []
    for intf in interfaces_db:
        lista_formatada.append({
            "name": intf["name"],
            "description": intf["description"],
            "switchport": {"access": {"vlan": intf["vlan"]}}
        })
    return {"Cisco-IOS-XE-native:GigabitEthernet": lista_formatada}

# 2. PATCH - Configurar Interface (Mudar VLAN)
@app.patch("/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet={name}")
async def update_interface(name: str, request: Request):
    body = await request.json()
    # Navegar no JSON para achar o ID da VLAN
    try:
        dados_intf = body.get("Cisco-IOS-XE-native:GigabitEthernet", {})
        nova_vlan = dados_intf.get("switchport", {}).get("access", {}).get("vlan")
        
        if nova_vlan:
            print(f"🔌 PORTA: Configurando GigabitEthernet{name} para VLAN {nova_vlan}")
            # Atualizar no "banco de dados"
            for intf in interfaces_db:
                if intf["name"] == name:
                    intf["vlan"] = int(nova_vlan)
                    break
    except Exception as e:
        print(f"Erro ao processar JSON: {e}")

    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)