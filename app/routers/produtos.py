from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import get_db
from app.services.produtos_service import ProdutoService
from app.security import validar_api_key

router = APIRouter(prefix="/produtos", tags=["Produtos"], dependencies=[Depends(validar_api_key)])

produto_service = ProdutoService()

@router.post("/", response_model=schemas.ProdutoResponse)
def cadastrar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return produto_service.criar_produto(db, produto)

@router.get("/", response_model=List[schemas.ProdutoResponse])
def listar_todos_os_produtos(apenas_ativos: bool = False, db: Session = Depends(get_db)):
    return produto_service.listar_produtos(db, apenas_ativos=apenas_ativos)

@router.put("/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(produto_id: int, dados: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return produto_service.atualizar_produto(db, produto_id, dados)

@router.delete("/{produto_id}")
def desativar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto_service.desativar_produto(db, produto_id)
    return {"mensagem": "Produto removido com sucesso"}

@router.get("/ranking", response_model=List[schemas.ProdutoStatus])
def ver_ranking_de_vendas(db: Session = Depends(get_db)):
    return produto_service.listar_produtos_com_estatisticas(db)