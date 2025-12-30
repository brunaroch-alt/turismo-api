from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import schemas
from app.database import get_db
from app.services.visitas_service import VisitaService
from app.security import validar_api_key

router = APIRouter(
    prefix="/visitas", 
    tags=["Visitas"], 
    dependencies=[Depends(validar_api_key)]
)

visita_service = VisitaService()

@router.post("/", response_model=schemas.VisitaResponse, summary="Registrar nova visita")
def criar_visita(visita: schemas.VisitaCreate, db: Session = Depends(get_db)):
    """
    Registra uma visita turística, vinculando um guia e os produtos vendidos.
    O sistema calcula automaticamente o faturamento total com base nos preços atuais.
    """
    return visita_service.registrar_visita(db, visita)

@router.get("/", response_model=List[schemas.VisitaResponse], summary="Listar todas as visitas")
def listar_historico_visitas(db: Session = Depends(get_db)):
    """
    Retorna o histórico completo de visitas realizadas.
    """
    return visita_service.listar_visitas(db)

@router.put("/{visita_id}", response_model=schemas.VisitaResponse, summary="Atualizar dados de uma visita")
def atualizar_visita(
    visita_id: int = Path(..., description="ID da visita que será editada"),
    dados: schemas.VisitaCreate = None, 
    db: Session = Depends(get_db)
):
    """
    Permite corrigir dados de uma visita e recalcula automaticamente os totais financeiros.
    """
    return visita_service.atualizar_visita(db, visita_id, dados) 

@router.delete("/{visita_id}", summary="Remover registro de visita")
def deletar_visita(
    visita_id: int = Path(..., description="ID da visita que vai excluída permanentemente"),
    db: Session = Depends(get_db)
):
    """
    Remove uma visita do banco de dados. 
    **Nota:** Esta ação é irreversível e remove o faturamento correspondente dos relatórios.
    """
    visita_service.deletar_visita(db, visita_id)
    return {"message": "Visita removida com sucesso. O faturamento foi atualizado."}

@router.get("/relatorio", response_model=schemas.RelatorioGeral, summary="Gerar relatório financeiro")
def obter_relatorio(
    data_inicio: Optional[datetime] = Query(None, description="Data inicial para o filtro - (YYYY-MM-DD)"), 
    data_fim: Optional[datetime] = Query(None, description="Data final para o filtro - (YYYY-MM-DD)"), 
    db: Session = Depends(get_db)
):
    """
    Gera um resumo financeiro, incluindo total de guias, produtos e arrecadação geral.
    É possível filtrar por um período específico de tempo.
    """
    return visita_service.gerar_relatorio_filtrado(db, data_inicio, data_fim)