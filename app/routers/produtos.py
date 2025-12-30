from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db
from app.services.produtos_service import ProdutoService
from app.security import validar_api_key

router = APIRouter(
    prefix="/produtos", 
    tags=["Produtos"], 
    dependencies=[Depends(validar_api_key)]
)

produto_service = ProdutoService()

@router.post("/", response_model=schemas.ProdutoResponse, summary="Cadastrar novo produto")
def cadastrar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    """
    Registra um novo produto no sistema com nome, preço e categoria.
    """
    return produto_service.criar_produto(db, produto)

@router.get("/", response_model=List[schemas.ProdutoResponse], summary="Listar produtos")
def listar_todos_os_produtos(apenas_ativos: bool = False, db: Session = Depends(get_db)):
    """
    Retorna a lista de produtos. Use o filtro 'apenas_ativos' para ocultar produtos desativados.
    """
    return produto_service.listar_produtos(db, apenas_ativos=apenas_ativos)

@router.put("/{produto_id}", response_model=schemas.ProdutoResponse, summary="Atualizar produto existente")
def atualizar_produto(
    produto_id: int = Path(..., description="ID numérico do produto a ser editado"), 
    dados: schemas.ProdutoCreate = None, 
    db: Session = Depends(get_db)
):
    """
    Atualiza as informações de um produto específico através do seu ID.
    """
    return produto_service.atualizar_produto(db, produto_id, dados)

@router.delete("/{produto_id}", summary="Desativar um produto")
def desativar_produto(
    produto_id: int = Path(..., description="É necessário informar o ID do produto na URL para realizar a remoção"), 
    db: Session = Depends(get_db)
):
    """
    Realiza a desativação lógica (soft delete) de um produto. 
    **Nota:** Não é possível realizar DELETE diretamente em /produtos sem o ID.
    """
    produto_service.desativar_produto(db, produto_id)
    return {"mensagem": "Produto removido com sucesso"}

@router.get("/ranking", response_model=List[schemas.ProdutoStatus], summary="Ver ranking de vendas")
def ver_ranking_de_vendas(db: Session = Depends(get_db)):
    """
    Gera um relatório dos produtos mais vendidos e faturamento histórico real.
    """
    return produto_service.listar_produtos_com_estatisticas(db)