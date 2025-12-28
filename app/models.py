from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Guia(Base):
    __tablename__ = "guias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    telefone = Column(String)
    ativo = Column(Boolean, default=True)

    visitas = relationship("Visita", back_populates="guia")

class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    qtd_turistas = Column(Integer)
    valor_taxa_guia = Column(Float)
    total_produtos = Column(Float, default=0.0)
    data_visita = Column(DateTime(timezone=True), server_default=func.now())
    guia_id = Column(Integer, ForeignKey("guias.id"), index=True)
    
    guia = relationship("Guia", back_populates="visitas")
    itens = relationship("VisitaProduto", back_populates="visita", cascade="all, delete-orphan")

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    preco = Column(Float)
    categoria = Column(String)
    ativo = Column(Boolean, default=True)

class VisitaProduto(Base):
    __tablename__ = "visita_produtos"
    
    id = Column(Integer, primary_key=True)
    visita_id = Column(Integer, ForeignKey("visitas.id", ondelete="CASCADE"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, default=1)
    preco_na_hora = Column(Float)

    visita = relationship("Visita", back_populates="itens")
    produto = relationship("Produto")
