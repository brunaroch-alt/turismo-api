from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ----------> GUIA

class GuiaBase(BaseModel):
    # Field ajuda a colocar exemplos reais no Swagger para facilitar o teste
    nome: str = Field(..., example="Macinho", description="Nome completo do guia")
    telefone: str = Field(..., example="11988887777", description="Telefone de contato com DDD")

class GuiaCreate(GuiaBase):
    # Por padrão, todo guia novo já nasce ativo
    ativo: bool = Field(True, description="Define se o guia pode ser vinculado a novas visitas")

class GuiaResponse(GuiaBase):
    id: int
    ativo: bool

    class Config:
        # Faz o Pydantic entender os objetos do banco de dados, no caso, SQLAlchemy
        from_attributes = True

class GuiaResumido(BaseModel):
    # Usei esse esquema mais simples para mostrar só o básico do guia dentro da visita
    nome: str
    telefone: str

    class Config:
        from_attributes = True


# ----------> VISITA

class ItemVenda(BaseModel):
    produto_id: int = Field(..., example=1)
    # gt=0 garante que ninguém tente vender quantidade negativa ou zero
    quantidade: int = Field(..., example=2, gt=0, description="Quantidade deve ser maior que zero")
    # Esse campo o usuário não preenche no POST, o Service vai calcular sozinho
    preco_na_hora: Optional[float] = Field(None, description="Preço unitário registrado no momento da venda")
    
    class Config:
        from_attributes = True

class VisitaBase(BaseModel):
    guia_id: int = Field(..., example=1)
    qtd_turistas: int = Field(..., example=5, description="Número de pessoas no grupo")
    valor_taxa_guia: float = Field(..., example=50.0, description="Valor cobrado pela condução do grupo")
    itens: List[ItemVenda]

class VisitaCreate(VisitaBase):
    pass

class VisitaResponse(BaseModel):
    id: int
    data_visita: datetime
    qtd_turistas: int
    total_produtos: float
    # Esse total é a soma da taxa do guia + o total dos produtos vendidos
    # Lembrando que ela não vai ser definida no models e sim no service
    total_arrecadado: float 
    guia: Optional[GuiaResumido]
    itens: List[ItemVenda] = []

    class Config:
        from_attributes = True


# ----------> PRODUTO

class ProdutoBase(BaseModel):
    nome: str = Field(..., example="Água Mineral 500ml")
    preco: float = Field(..., example=5.0)
    categoria: str = Field(..., example="Bebidas")

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int
    ativo: bool

    class Config:
        from_attributes = True

class ProdutoStatus(BaseModel):
    # Esse esquema é especial para o ranking de produtos mais vendidos
    id: int
    ativo: bool
    nome: str
    categoria: str
    preco: float
    unidades_vendidas: int 
    faturamento_total: float 

    class Config:
        from_attributes = True


# ----------> RELATÓRIO

class RelatorioGeral(BaseModel):
    # Campos que resumem a saúde financeira da 'empresa' no período selecionado
    total_taxas_guias: float = Field(..., description="Soma de todas as taxas de guias no período")
    total_produtos: float = Field(..., description="Soma de todas as vendas de produtos no período")
    faturamento_total_geral: float = Field(..., description="Soma total arrecadada (Taxas + Produtos)")
    quantidade_visitas: int = Field(..., description="Total de registros de visitas processados")