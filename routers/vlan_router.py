# routers/vlan_router.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
# Atualiza os imports:
from vlan_manager import get_vlans, create_vlan, delete_vlan, get_interfaces, assign_vlan

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def index(request: Request):
    vlans = get_vlans()
    return templates.TemplateResponse("index.html", {"request": request, "vlans": vlans})

# --- ROTAS DE CONFIGURAÇÃO DE PORTA ---

@router.get("/assign")
async def assign_page(request: Request):
    # Precisamos das VLANs (para o dropdown) e das Interfaces (para ver o estado atual)
    vlans = get_vlans()
    interfaces = get_interfaces()
    return templates.TemplateResponse("assign_port.html", {
        "request": request, 
        "vlans": vlans, 
        "interfaces": interfaces
    })

@router.post("/assign")
async def assign_post(request: Request, interface_name: str = Form(...), vlan_id: int = Form(...)):
    sucesso, msg = assign_vlan(interface_name, vlan_id)
    print(f"Atribuir Porta: {msg}")
    return RedirectResponse(url="/assign", status_code=303)

# ... (Mantém as outras rotas: /add, /delete)
@router.post("/add")
async def add(request: Request, vlan_id: int = Form(...), vlan_name: str = Form(...)):
    create_vlan(vlan_id, vlan_name)
    return RedirectResponse(url="/", status_code=303)

@router.get("/delete/{vlan_id}")
async def delete_route(vlan_id: int):
    delete_vlan(vlan_id)
    return RedirectResponse(url="/", status_code=303)

# routers/vlan_router.py

# ... (MANTÉM OS IMPORTS ANTERIORES)

# 1. ATUALIZAR ESTA ROTA EXISTENTE
@router.get("/topology/{vlan_id}")
async def vlan_topology(request: Request, vlan_id: int):
    todas_vlans = get_vlans()
    vlan_info = next((v for v in todas_vlans if v['id'] == vlan_id), None)
    
    todas_interfaces = get_interfaces()
    
    # Lista 1: Quem pertence a esta VLAN
    dispositivos_conectados = [
        intf for intf in todas_interfaces 
        if int(intf['switchport']['access']['vlan']) == vlan_id
    ]

    # Lista 2: Quem NÃO pertence (Disponíveis para adicionar)
    # Excluímos a VLAN atual da lista
    dispositivos_disponiveis = [
        intf for intf in todas_interfaces 
        if int(intf['switchport']['access']['vlan']) != vlan_id
    ]

    return templates.TemplateResponse("vlan_topology.html", {
        "request": request,
        "vlan": vlan_info,
        "devices": dispositivos_conectados,
        "available": dispositivos_disponiveis # <--- Nova lista enviada
    })

# 2. NOVA ROTA PARA PROCESSAR A EDIÇÃO NA TOPOLOGIA
@router.post("/topology/update")
async def topology_update(
    request: Request, 
    interface_name: str = Form(...), 
    target_vlan: int = Form(...),
    return_to_vlan: int = Form(...) # Para saber para onde voltar
):
    # Usa a função que já criámos antes para mover a porta
    assign_vlan(interface_name, target_vlan)
    
    # Recarrega a página da topologia atual
    return RedirectResponse(url=f"/topology/{return_to_vlan}", status_code=303)