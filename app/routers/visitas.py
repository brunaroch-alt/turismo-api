from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import get_db
from app.services.visitas_service import VisitaService
from datetime import datetime
from typing import Optional
from app.security import validar_api_key

router = APIRouter(prefix="/visitas", tags=["Visitas"], dependencies=[Depends(validar_api_key)])

visita_service = VisitaService()

@router.post("/", response_model=schemas.VisitaResponse)
def criar_visita(visita: schemas.VisitaCreate, db: Session = Depends(get_db)):
    return visita_service.registrar_visita(db, visita)

@router.get("/", response_model=List[schemas.VisitaResponse])
def listar_historico_visitas(db: Session = Depends(get_db)):
    return visita_service.listar_visitas(db)

@router.put("/{visita_id}", response_model=schemas.VisitaResponse)
def atualizar_visita(visita_id: int, dados: schemas.VisitaCreate, db: Session = Depends(get_db)):
    return visita_service.atualizar_visita(db, visita_id, dados) 

@router.delete("/{visita_id}")
def deletar_visita(visita_id: int, db: Session = Depends(get_db)):
    visita_service.deletar_visita(db, visita_id)
    return {"message": "Visita removida com sucesso. O faturamento foi atualizado."}

@router.get("/relatorio", response_model=schemas.RelatorioGeral)
def obter_relatorio(data_inicio: Optional[datetime] = None, data_fim: Optional[datetime] = None, db: Session = Depends(get_db)):
    return visita_service.gerar_relatorio_filtrado(db, data_inicio, data_fim)