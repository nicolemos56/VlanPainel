# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import vlan_router
from fastapi.responses import FileResponse

app = FastAPI(title="VLAN Painel")

# inclui router
app.include_router(vlan_router.router)

# servir ficheiros estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# favicon opcional
@app.get("/favicon.ico")
def favicon():
    try:
        return FileResponse("static/favicon.ico")
    except:
        return {}
