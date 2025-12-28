from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

"""
Base - Infos base da classe

Create - Usada para receber os dados de criação/edição

Response - Usada para devolver os dados; Resposta.
"""
# ----------> guia

class GuiaBase(BaseModel):
    nome: str
    telefone: str

class GuiaCreate(GuiaBase):
    ativo: bool = True
    pass

class GuiaResponse(GuiaBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True # Isso permite que o Pydantic leia dados do SQLAlchemy

# Schema simples só para mostrar o nome/telefone do guia dentro da visita
class GuiaResumido(BaseModel):
    nome: str
    telefone: str

    class Config:
        from_attributes = True


# ----------> visita

class ItemVenda(BaseModel):
    produto_id: int
    quantidade: int
    preco_na_hora: Optional[float] = None
    
    class Config:
        from_attributes = True

class VisitaBase(BaseModel):
    guia_id: int
    qtd_turistas: int
    valor_taxa_guia: float
    itens: List[ItemVenda]

class VisitaCreate(VisitaBase):
    pass

class VisitaResponse(BaseModel):
    id: int
    data_visita: datetime
    qtd_turistas: int
    total_produtos: float
    total_arrecadado: float 
    guia: Optional[GuiaResumido] 
    itens: List[ItemVenda] = []

    class Config:
        from_attributes = True

# ----------> produto

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    categoria: str 

class ProdutoCreate(ProdutoBase):
    ativo: bool = True
    pass

class ProdutoResponse(ProdutoBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True

class ProdutoStatus(BaseModel):
    id: int
    ativo: bool
    nome: str
    categoria: str
    preco: float
    unidades_vendidas: int 
    faturamento_total: float 

    class Config:
        from_attributes = True

# ----------> relatório

class RelatorioGeral(BaseModel):
    total_taxas_guias: float
    total_produtos: float 
    faturamento_total_geral: float
    quantidade_visitas: int