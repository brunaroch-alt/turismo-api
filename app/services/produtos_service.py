from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import func

class ProdutoService:
    def criar_produto(self, db: Session, produto: schemas.ProdutoCreate):
        try:
            
            if produto.preco < 0:
                raise HTTPException(status_code=400, detail="O preço do produto não pode ser negativo.") 

            novo = models.Produto(**produto.model_dump()) # lembrar: transformando os dados do swagger (pydantic) em um dicionário comum do python. (**) pra desempacotar

            db.add(novo)
            db.commit()
            db.refresh(novo)
            
            return novo
        except HTTPException as error:

            raise error
        except Exception:

            db.rollback()

            raise HTTPException(status_code=500, detail='Erro interno ao criar produto.')

    def buscar_por_id(self, db: Session, produto_id: int):
        produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()

        if not produto:

            raise HTTPException(status_code=404, detail=f'Produto com ID {produto_id} não encontrado.')
        
        return produto
    
    def listar_produtos(self, db: Session, apenas_ativos: bool = False):
        query = db.query(models.Produto)

        if apenas_ativos:

            return query.filter(models.Produto.ativo == True).all()
        
        return query.all()

    def atualizar_produto(self, db: Session, produto_id: int, novos_dados: schemas.ProdutoCreate):
        produto_existente = self.buscar_por_id(db, produto_id)

        try:

            if novos_dados.preco < 0:
                raise HTTPException(status_code=400, detail="O preço atualizado não pode ser negativo.")

            produto_existente.nome = novos_dados.nome
            produto_existente.preco = novos_dados.preco
            produto_existente.categoria = novos_dados.categoria
            
            db.commit()
            db.refresh(produto_existente)

            return produto_existente
        except HTTPException as error:

            raise error
        except Exception:

            db.rollback()

            raise HTTPException(status_code=500, detail='Erro ao atualizar produto.')

    def desativar_produto(self, db: Session, produto_id: int):
        produto = self.buscar_por_id(db, produto_id)

        try:

            produto.ativo = False
            db.commit()

            return True
        except Exception:

            db.rollback()

            raise HTTPException(status_code=500, detail='Erro ao desativar produto.')
    
    def listar_produtos_com_estatisticas(self, db: Session):
        try:

            estatisticas_query = db.query(
                models.VisitaProduto.produto_id, 
                func.sum(models.VisitaProduto.quantidade).label("total_unidades"),
                func.sum(models.VisitaProduto.quantidade * models.VisitaProduto.preco_na_hora).label("faturamento_real")
            ).group_by(models.VisitaProduto.produto_id).all()


            mapa_vendas = {
                item.produto_id: {
                    "unidades": item.total_unidades, 
                    "faturamento": item.faturamento_real
                } for item in estatisticas_query
            }

            produtos = db.query(models.Produto).all()
            
            ranking = []
            for p in produtos:
                
                dados_venda = mapa_vendas.get(p.id, {"unidades": 0, "faturamento": 0.0})
                
                ranking.append({
                    "id": p.id,
                    "ativo": p.ativo,
                    "nome": p.nome,
                    "categoria": p.categoria,
                    "preco": p.preco,
                    "unidades_vendidas": dados_venda["unidades"],
                    "faturamento_total": dados_venda["faturamento"]
                })
            
   
            ranking = sorted(ranking, key=lambda x: x['faturamento_total'], reverse=True)

            return ranking
        except Exception:

            raise HTTPException(status_code=500, detail="Erro ao gerar ranking de estatísticas.")