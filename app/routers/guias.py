from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.services.guias_service import GuiaService
from typing import List
from app.security import validar_api_key

router = APIRouter(prefix="/guias", tags=["Guias"], dependencies=[Depends(validar_api_key)])

guia_service = GuiaService()

@router.post("/", response_model=schemas.GuiaResponse)
def criar_novo_guia(guia: schemas.GuiaCreate, db: Session = Depends(get_db)):
    return guia_service.criar_guia(db, guia)

@router.get("/", response_model=List[schemas.GuiaResponse])
def listar_todos_os_guias(apenas_ativos: bool = False, db: Session = Depends(get_db)):
    return guia_service.listar_guias(db, apenas_ativos=apenas_ativos)

@router.get("/{guia_id}", response_model=schemas.GuiaResponse)
def buscar_guia(guia_id: int, db: Session = Depends(get_db)):
    return guia_service.buscar_por_id(db, guia_id)

@router.put("/{guia_id}", response_model=schemas.GuiaResponse)
def atualizar_guia(guia_id: int, novos_dados: schemas.GuiaCreate, db: Session = Depends(get_db)):
    return guia_service.atualizar_guia(db, guia_id, novos_dados)

@router.delete("/{guia_id}")
def desativar_guia(guia_id: int, db: Session = Depends(get_db)):
    guia_service.desativar_guia(db, guia_id)
    return {"message": "Guia desativado com sucesso (os dados históricos foram preservados)"}