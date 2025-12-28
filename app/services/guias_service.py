from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas

class GuiaService:
    def criar_guia(self, db: Session, guia_data: schemas.GuiaCreate):
        try:
            novo_guia = models.Guia(
                nome=guia_data.nome,
                telefone=guia_data.telefone,
                ativo=True
            )

            db.add(novo_guia)
            db.commit()
            db.refresh(novo_guia)

            return novo_guia
        except Exception:

            db.rollback()

            raise HTTPException(status_code=500, detail='Erro interno ao cadastrar o guia.')

    def listar_guias(self, db: Session, apenas_ativos: bool = False):
        query = db.query(models.Guia)

        if apenas_ativos:

            return query.filter(models.Guia.ativo == True).all()
        
        return query.all()

    def buscar_por_id(self, db: Session, guia_id: int):
        guia = db.query(models.Guia).filter(models.Guia.id == guia_id).first()

        if not guia:

            raise HTTPException(status_code=404, detail=f'Guia com ID {guia_id} não encontrado.')
        
        return guia

    def desativar_guia(self, db: Session, guia_id: int):
        guia = self.buscar_por_id(db, guia_id)

        try:

            guia.ativo = False
            db.commit()

            return True
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail='Erro ao desativar o guia.')

    def atualizar_guia(self, db: Session, guia_id: int, novos_dados: schemas.GuiaCreate):
        guia_existente = self.buscar_por_id(db, guia_id)

        try:

            guia_existente.nome = novos_dados.nome
            guia_existente.telefone = novos_dados.telefone
            guia_existente.ativo = novos_dados.ativo
            
            db.commit()
            db.refresh(guia_existente)

            return guia_existente
        except Exception:

            db.rollback()

            raise HTTPException(status_code=500, detail='Erro ao atualizar os dados do guia.')