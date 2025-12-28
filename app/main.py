from fastapi import FastAPI
from app.routers import guias, visitas, produtos

app = FastAPI(title="Turismo API")

app.include_router(guias.router)
app.include_router(visitas.router)
app.include_router(produtos.router)

@app.get("/")
def home():
    return {"mensagem": "API online!"}