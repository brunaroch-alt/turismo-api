from fastapi import FastAPI
from app.routers import guias, visitas, produtos

app = FastAPI(
    title="Turismo API",
    description="API para gestão de faturamento turístico e controle de guias.",
    version="1.0.0"
)

app.include_router(guias.router)
app.include_router(visitas.router)
app.include_router(produtos.router)

@app.get("/", tags=["Home"])
def home():
    return {
        "status": "online", 
        "mensagem": "Bem-vindo à Turismo API. Acesse /docs para a documentação."
    }