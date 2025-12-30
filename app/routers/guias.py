from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.services.guias_service import GuiaService
from typing import List
from app.security import validar_api_key

router = APIRouter(
    prefix="/guias", 
    tags=["Guias"], 
    dependencies=[Depends(validar_api_key)]
)

guia_service = GuiaService()

@router.post("/", response_model=schemas.GuiaResponse, summary="Criar um novo guia")
def criar_novo_guia(guia: schemas.GuiaCreate, db: Session = Depends(get_db)):
    """
    Cadastra um guia no sistema. Por padrão, o guia é criado com o status 'ativo'.
    """
    return guia_service.criar_guia(db, guia)

@router.get("/", response_model=List[schemas.GuiaResponse], summary="Listar guias cadastrados")
def listar_todos_os_guias(apenas_ativos: bool = False, db: Session = Depends(get_db)):
    """
    Retorna a lista de todos os guias. 
    Marque 'apenas_ativos' como verdadeiro para filtrar apenas guias disponíveis para novas visitas.
    """
    return guia_service.listar_guias(db, apenas_ativos=apenas_ativos)

@router.get("/{guia_id}", response_model=schemas.GuiaResponse, summary="Buscar guia por ID")
def buscar_guia(
    guia_id: int = Path(..., description="ID numérico do guia que deseja consultar"), 
    db: Session = Depends(get_db)
):
    """
    Retorna as informações detalhadas de um guia específico.
    """
    return guia_service.buscar_por_id(db, guia_id)

@router.put("/{guia_id}", response_model=schemas.GuiaResponse, summary="Atualizar dados de um guia")
def atualizar_guia(
    guia_id: int = Path(..., description="ID do guia a ser atualizado"), 
    novos_dados: schemas.GuiaCreate = None, 
    db: Session = Depends(get_db)
):
    """
    Permite alterar o nome, telefone ou status de atividade de um guia existente.
    """
    return guia_service.atualizar_guia(db, guia_id, novos_dados)

@router.delete("/{guia_id}", summary="Desativar um guia")
def desativar_guia(
    guia_id: int = Path(..., description="É necessário informar o ID do guia na URL para desativá-lo"), 
    db: Session = Depends(get_db)
):
    """
    Desativa o guia no sistema. 
    **Importante:** Os dados não são apagados permanentemente para preservar o histórico das visitas realizadas.
    """
    guia_service.desativar_guia(db, guia_id)
    return {"message": "Guia desativado com sucesso (os dados históricos foram preservados)"}