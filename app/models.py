from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Guia(Base):
    __tablename__ = "guias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    telefone = Column(String)
    # Controle de quem ainda está trabalhando na 'empresa'
    ativo = Column(Boolean, default=True)

    # Ligação para conseguir ver todas as visitas que este guia já fez
    visitas = relationship("Visita", back_populates="guia")

class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    qtd_turistas = Column(Integer)
    valor_taxa_guia = Column(Float)
    total_produtos = Column(Float, default=0.0)
    # O server_default garante que a data seja gravada automaticamente no momento da criação
    data_visita = Column(DateTime(timezone=True), server_default=func.now())
    
    # Chave estrangeira para saber qual guia fez a visita
    guia_id = Column(Integer, ForeignKey("guias.id"), index=True)
    
    guia = relationship("Guia", back_populates="visitas")
    
    # O cascade="all, delete-orphan" serve para que, se eu apagar a visita, 
    # os itens vendidos nela também sejam apagados automaticamente
    itens = relationship("VisitaProduto", back_populates="visita", cascade="all, delete-orphan")

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    preco = Column(Float)
    categoria = Column(String)
    # Usado para o "soft delete".
    ativo = Column(Boolean, default=True)

class VisitaProduto(Base):
    """
    Esta tabela serve para ligar os produtos às visitas.
    """
    __tablename__ = "visita_produtos"
    
    id = Column(Integer, primary_key=True)
    visita_id = Column(Integer, ForeignKey("visitas.id", ondelete="CASCADE"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, default=1)
    
    # Guardo o preço aqui para o faturamento não mudar se o preço do produto for alterado depois
    preco_na_hora = Column(Float)

    visita = relationship("Visita", back_populates="itens")
    produto = relationship("Produto")