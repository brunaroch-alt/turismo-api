from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime, timedelta

class VisitaService:
    def registrar_visita(self, db: Session, dados_visita: schemas.VisitaCreate):
        try:
            guia = db.query(models.Guia).filter(models.Guia.id == dados_visita.guia_id).first()

            if not guia:

                raise HTTPException(status_code=404, detail=f'Guia com ID {dados_visita.guia_id} não encontrado.')
            
            if not guia.ativo:

                raise HTTPException(status_code=400, detail='Não é possível registrar visita para um guia inativo.')

            ids_enviados = [item.produto_id for item in dados_visita.itens]

            produtos_no_banco = db.query(models.Produto).filter(models.Produto.id.in_(ids_enviados)).all()

            if len(produtos_no_banco) != len(set(ids_enviados)):
                raise HTTPException(status_code=400, detail='Um ou mais IDs de produtos são inválidos ou não existem.')

            mapa_precos = {p.id: p.preco for p in produtos_no_banco}

            soma_produtos = 0.0
            objetos_itens = []


            for item in dados_visita.itens:
                preco_atual = mapa_precos.get(item.produto_id)

                if preco_atual:

                    soma_produtos += (preco_atual * item.quantidade)
    
                    objetos_itens.append(models.VisitaProduto(
                    produto_id=item.produto_id,
                    quantidade=item.quantidade,
                    preco_na_hora=preco_atual
                ))

            nova_visita = models.Visita(
                guia_id=dados_visita.guia_id,
                qtd_turistas=dados_visita.qtd_turistas,
                valor_taxa_guia=dados_visita.valor_taxa_guia,
                total_produtos=soma_produtos,
                itens=objetos_itens
            )

            db.add(nova_visita)
            db.commit()
            db.refresh(nova_visita) # não esquecer do refresh para pegar de voltar os dados
            
            nova_visita.total_arrecadado = nova_visita.valor_taxa_guia + nova_visita.total_produtos

            return nova_visita
        
        except HTTPException as error:

            db.rollback()

            raise error
        except Exception:

            db.rollback()

            raise HTTPException(status_code=500, detail='Erro interno ao registrar visita.')
        

    def listar_visitas(self, db: Session):
        visitas = db.query(models.Visita).all()
        
        resultado = []

        for v in visitas:
            total_geral = v.valor_taxa_guia + v.total_produtos

            visita_schema = schemas.VisitaResponse(
                id=v.id,
                guia_id=v.guia_id,
                data_visita=v.data_visita,
                qtd_turistas=v.qtd_turistas,
                valor_taxa_guia=v.valor_taxa_guia,
                total_produtos=v.total_produtos,
                total_arrecadado=total_geral,
                guia=v.guia,
                itens=v.itens
            )

            resultado.append(visita_schema)

        return resultado
    
    def buscar_por_id(self, db: Session, visita_id: int):
        visita = db.query(models.Visita).filter(models.Visita.id == visita_id).first()

        if not visita:
            raise HTTPException(status_code=404, detail='Visita não encontrada.')
        
        return visita
    
    def deletar_visita(self, db: Session, visita_id: int):
        visita = self.buscar_por_id(db, visita_id)

        try:

            db.delete(visita)
            db.commit()

            return True
        except Exception:

            db.rollback()

            raise HTTPException(status_code=500, detail='Erro ao deletar visita.') 
 
    def atualizar_visita(self, db: Session, visita_id: int, dados: schemas.VisitaCreate):
        visita_existente = self.buscar_por_id(db, visita_id)

        try:
            
            ids_enviados = [item.produto_id for item in dados.itens]

            produtos_no_banco = db.query(models.Produto).filter(models.Produto.id.in_(ids_enviados)).all()

            if len(produtos_no_banco) != len(set(ids_enviados)):
                raise HTTPException(status_code=400, detail='Um ou mais IDs de produtos são inválidos ou não existem.')
            
            mapa_precos = {p.id: p.preco for p in produtos_no_banco}
            
            visita_existente.guia_id = dados.guia_id
            visita_existente.qtd_turistas = dados.qtd_turistas
            visita_existente.valor_taxa_guia = dados.valor_taxa_guia

            db.query(models.VisitaProduto).filter(models.VisitaProduto.visita_id == visita_id).delete()

            soma_produtos = 0.0
            novos_itens = []
            for item in dados.itens:
                preco_atual = mapa_precos.get(item.produto_id)

                if preco_atual:

                    soma_produtos += (preco_atual * item.quantidade)

                    novos_itens.append(models.VisitaProduto(
                        visita_id=visita_id,
                        produto_id=item.produto_id,
                        quantidade=item.quantidade,
                        preco_na_hora=preco_atual
                    ))

            visita_existente.total_produtos = soma_produtos
            visita_existente.itens = novos_itens
            
            db.commit()
            db.refresh(visita_existente)

            visita_existente.total_arrecadado = visita_existente.valor_taxa_guia + visita_existente.total_produtos
            
            return visita_existente
        except HTTPException as error:
            db.rollback()
            raise error
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail='Erro ao atualizar visita.')
    
    def gerar_relatorio_filtrado(self, db: Session, data_inicio: datetime = None, data_fim: datetime = None):
        if data_inicio and data_fim and data_inicio > data_fim:
            raise HTTPException(status_code=400, detail='A data de início não pode ser maior que a data de fim.')

        query = db.query(models.Visita)
    
        if data_inicio:
            query = query.filter(models.Visita.data_visita >= data_inicio)
            
        if data_fim:
            data_fim_ajustada = data_fim + timedelta(days=1)
            query = query.filter(models.Visita.data_visita < data_fim_ajustada)
            
        visitas = query.all()
        
        taxas = sum(v.valor_taxa_guia for v in visitas)
        tot_produtos = sum(v.total_produtos for v in visitas)
        
        return {
            "total_taxas_guias": taxas,
            "total_produtos": tot_produtos,
            "faturamento_total_geral": taxas + tot_produtos,
            "quantidade_visitas": len(visitas)
        }