from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas

class GuiaService:
    def criar_guia(self, db: Session, guia_data: schemas.GuiaCreate):
        try:
            # Crio o guia usando os dados que vieram do Pydantic
            novo_guia = models.Guia(
                nome=guia_data.nome,
                telefone=guia_data.telefone,
                ativo=guia_data.ativo
            )

            db.add(novo_guia)
            db.commit()
            db.refresh(novo_guia) # Pego os dados atualizados (como o ID gerado)

            return novo_guia
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail='Erro interno ao cadastrar o guia.')

    def listar_guias(self, db: Session, apenas_ativos: bool = False):
        query = db.query(models.Guia)

        # Se o filtro de ativos estiver ligado, mostro só quem pode trabalhar
        if apenas_ativos:
            return query.filter(models.Guia.ativo == True).all()
        
        return query.all()

    def buscar_por_id(self, db: Session, guia_id: int):
        # Procuro o guia pelo ID. Se não achar, já mando o erro 404
        guia = db.query(models.Guia).filter(models.Guia.id == guia_id).first()

        if not guia:
            raise HTTPException(status_code=404, detail=f'Não encontramos nenhum guia com o ID {guia_id}. Verifique o ID e tente novamente.')
        
        return guia

    def desativar_guia(self, db: Session, guia_id: int):
        # Primeiro busco o guia para ver se ele existe
        guia = self.buscar_por_id(db, guia_id)

        # Se ele já estiver desativado, não preciso fazer nada, então aviso o usuário
        if not guia.ativo:
            raise HTTPException(status_code=400, detail='Este guia já se encontra desativado no sistema.')

        try:
            # Faço o "soft delete" mudando o status para inativo
            guia.ativo = False
            db.commit()

            return True
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail='Não foi possível desativar o guia no momento.')

    def atualizar_guia(self, db: Session, guia_id: int, novos_dados: schemas.GuiaCreate):
        # Verifico se o guia existe antes de tentar mudar qualquer coisa
        guia_existente = self.buscar_por_id(db, guia_id)

        try:
            # Atualizo os campos com as novas informações
            guia_existente.nome = novos_dados.nome
            guia_existente.telefone = novos_dados.telefone
            guia_existente.ativo = novos_dados.ativo
            
            db.commit()
            db.refresh(guia_existente)

            return guia_existente
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail='Erro ao atualizar os dados do guia.')