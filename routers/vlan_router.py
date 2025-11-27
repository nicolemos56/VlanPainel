from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from vlan_manager import get_vlans, create_vlan, delete_vlan, get_interfaces, assign_vlan

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# --- HOMEPAGE ---
@router.get("/")
async def index(request: Request):
    vlans = get_vlans()
    return templates.TemplateResponse("index.html", {"request": request, "vlans": vlans})

# --- ADICIONAR VLAN ---
@router.get("/add")  # <--- ESTA ERA A QUE FALTAVA
async def add_form(request: Request):
    return templates.TemplateResponse("add_vlan.html", {"request": request})

@router.post("/add")
async def add(request: Request, vlan_id: int = Form(...), vlan_name: str = Form(...)):
    create_vlan(vlan_id, vlan_name)
    return RedirectResponse(url="/", status_code=303)

# --- APAGAR VLAN ---
@router.get("/delete/{vlan_id}")
async def delete_route(vlan_id: int):
    delete_vlan(vlan_id)
    return RedirectResponse(url="/", status_code=303)

# --- TOPOLOGIA ---
@router.get("/topology/{vlan_id}")
async def vlan_topology(request: Request, vlan_id: int):
    todas_vlans = get_vlans()
    vlan_info = next((v for v in todas_vlans if v['id'] == vlan_id), None)
    
    todas_interfaces = get_interfaces()
    
    # Filtra dispositivos nesta VLAN
    dispositivos_conectados = [
        intf for intf in todas_interfaces 
        if int(intf['switchport']['access']['vlan']) == vlan_id
    ]

    # Filtra dispositivos disponiveis (noutras VLANs)
    dispositivos_disponiveis = [
        intf for intf in todas_interfaces 
        if int(intf['switchport']['access']['vlan']) != vlan_id
    ]

    return templates.TemplateResponse("vlan_topology.html", {
        "request": request,
        "vlan": vlan_info,
        "devices": dispositivos_conectados,
        "available": dispositivos_disponiveis
    })

@router.post("/topology/update")
async def topology_update(
    request: Request, 
    interface_name: str = Form(...), 
    target_vlan: int = Form(...),
    return_to_vlan: int = Form(...)
):
    assign_vlan(interface_name, target_vlan)
    return RedirectResponse(url=f"/topology/{return_to_vlan}", status_code=303)

# --- GERIR PORTAS (ASSIGN) ---
@router.get("/assign")
async def assign_page(request: Request):
    vlans = get_vlans()
    interfaces = get_interfaces()
    return templates.TemplateResponse("assign_port.html", {
        "request": request, 
        "vlans": vlans, 
        "interfaces": interfaces
    })

@router.post("/assign")
async def assign_post(request: Request, interface_name: str = Form(...), vlan_id: int = Form(...)):
    assign_vlan(interface_name, vlan_id)
    return RedirectResponse(url="/assign", status_code=303)