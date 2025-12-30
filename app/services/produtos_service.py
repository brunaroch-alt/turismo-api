from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import func

class ProdutoService:
    def criar_produto(self, db: Session, produto: schemas.ProdutoCreate):
        try:
            # Não faz sentido vender produto com preço negativo, então barramos aqui
            if produto.preco < 0:
                raise HTTPException(status_code=400, detail="O preço do produto não pode ser negativo.") 

            # Aqui eu transformo os dados que vêm do Swagger em um modelo que o banco entende
            # Usei o model_dump() para facilitar a conversão
            novo = models.Produto(**produto.model_dump()) 

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
        # Procuro o produto pelo ID; se não existir, já retorno erro 404 de uma vez
        produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()

        if not produto:
            raise HTTPException(status_code=404, detail=f'Produto com ID {produto_id} não encontrado.')
        
        return produto
    
    def listar_produtos(self, db: Session, apenas_ativos: bool = False):
        query = db.query(models.Produto)

        # Se o usuário quiser apenas os ativos, aplico o filtro aqui
        if apenas_ativos:
            return query.filter(models.Produto.ativo == True).all()
        
        return query.all()

    def atualizar_produto(self, db: Session, produto_id: int, novos_dados: schemas.ProdutoCreate):
        produto_existente = self.buscar_por_id(db, produto_id)

        try:
            if novos_dados.preco < 0:
                raise HTTPException(status_code=400, detail="O preço atualizado não pode ser negativo.")

            # Atualizo campo por campo para ter certeza do que está sendo alterado no banco
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
            # Importante: não apago o produto para não estragar o histórico das visitas antigas
            # Apenas mudo o status para inativo
            produto.ativo = False
            db.commit()

            return True
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail='Erro ao desativar produto.')
    
    def listar_produtos_com_estatisticas(self, db: Session):
        try:
            # Peço ao banco para somar as quantidades e o faturamento real
            # Faço o cálculo direto no SQL (quantidade * preço gravado na hora da visita)
            estatisticas_query = db.query(
                models.VisitaProduto.produto_id, 
                func.sum(models.VisitaProduto.quantidade).label("total_unidades"),
                func.sum(models.VisitaProduto.quantidade * models.VisitaProduto.preco_na_hora).label("faturamento_real")
            ).group_by(models.VisitaProduto.produto_id).all()

            # Crio um dicionário para achar os dados de venda mais fácil depois
            mapa_vendas = {
                item.produto_id: {
                    "unidades": item.total_unidades, 
                    "faturamento": item.faturamento_real
                } for item in estatisticas_query
            }

            produtos = db.query(models.Produto).all()
            
            ranking = []
            for p in produtos:
                # Se o produto nunca foi vendido, coloco 0 para não dar erro no retorno
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
            
            # Ordeno a lista para mostrar primeiro quem faturou mais
            ranking = sorted(ranking, key=lambda x: x['faturamento_total'], reverse=True)

            return ranking
        except Exception:
            raise HTTPException(status_code=500, detail="Erro ao gerar ranking de estatísticas.")