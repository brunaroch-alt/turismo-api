# Turismo API

API REST desenvolvida com FastAPI para controle de visitas turísticas, guias e vendas de produtos, permitindo o registro completo das visitas, cálculo de faturamento e geração de relatórios.

O projeto simula um cenário real de um ponto turístico, onde cada visita pode envolver um guia, cobrança de taxa e venda de produtos, mantendo o histórico correto de preços e dados financeiros.

---

## Funcionalidades

* Cadastro, listagem, atualização e desativação de guias
* Cadastro, listagem, atualização e desativação de produtos
* Registro de visitas turísticas
* Associação de produtos vendidos a cada visita
* Histórico de Preços: O sistema grava o preço do produto no exato momento da venda (preco_na_hora), garantindo que relatórios financeiros antigos não sejam alterados caso o preço do produto mude hoje.
* Cálculo automático de:

  * Total de produtos vendidos por visita
  * Total arrecadado (taxa do guia + produtos)
* Geração de relatórios financeiros com filtro por período
* Ranking de produtos por faturamento e unidades vendidas
* Autenticação via API Key

---

## Tecnologias utilizadas

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* Uvicorn
* dotenv
* Alembic (migrations de banco de dados)

---

## Estrutura do projeto

```
app/
├── main.py
├── models.py
├── schemas.py
├── database.py
├── security.py
├── routers/
│   ├── guias.py
│   ├── visitas.py
│   └── produtos.py
├── services/
│   ├── guias_service.py
│   ├── visitas_service.py
│   └── produtos_service.py
```

---

## Regras de negócio implementadas

* Não é possível registrar visitas para guias inativos
* Apenas produtos existentes podem ser vinculados a uma visita
* O preço do produto é armazenado no momento da venda, garantindo histórico correto
* Guias e produtos são desativados (soft delete), preservando dados históricos
* Relatórios consideram filtros de data e retornam valores consolidados

---

## Autenticação

A API utiliza autenticação via API Key.

É necessário enviar o header abaixo em todas as requisições:

```
X-API-KEY: sua_api_key
```

A chave deve ser configurada no arquivo `.env`:

```
API_KEY_TURISMO=sua_api_key
```

---

## Migrations com Alembic

O projeto utiliza **Alembic** para controle de versões do banco de dados e criação de migrations.

Principais comandos utilizados:

```
alembic revision --autogenerate -m "mensagem da migration"
alembic upgrade head
```

O Alembic garante que a estrutura do banco acompanhe a evolução do projeto de forma segura e versionada.

---

## Como executar o projeto

1. Clone o repositório
2. Crie um ambiente virtual
3. Instale as dependências
4. Configure o arquivo `.env`
5. Execute a aplicação

Exemplo:

```
uvicorn app.main:app --reload
```

A API ficará disponível em:

```
http://127.0.0.1:8000
```

A documentação automática pode ser acessada em:

```
http://127.0.0.1:8000/docs
```

---

## Endpoints principais

* `/guias`
* `/produtos`
* `/visitas`
* `/visitas/relatorio`
* `/produtos/ranking`

Todos os endpoints exigem autenticação via API Key.

---

## Motivação do projeto

Este projeto foi inspirado em um cenário real de turismo comunitário, onde guias levam grupos de visitantes para conhecer pontos turísticos locais, com explicações históricas, além da venda de produtos artesanais e bebidas.

A ideia surgiu da necessidade de organizar informações como quantidade de visitantes, valores arrecadados, produtos vendidos e atuação dos guias, de forma simples e confiável. Durante meus estudos, percebi que uma API seria uma solução adequada para centralizar essas informações e permitir futuras integrações com diferentes interfaces.

O foco do projeto está na modelagem correta das regras de negócio, no controle financeiro e na preservação do histórico das informações, simulando um sistema que poderia ser utilizado em um contexto real.

---

## Objetivo do projeto

Este projeto foi desenvolvido com foco em aprendizado prático de APIs REST, organização de código, regras de negócio e integração entre FastAPI, SQLAlchemy e Pydantic.

Ele faz parte do meu portfólio como estudante de Análise e Desenvolvimento de Sistemas, com interesse em backend e análise de dados.

---

## Próximas melhorias (Meus planos de aprendizado)

* Exportação de dados consolidados para formatos Excel (.xlsx) e PDF.
* Implementação de testes unitários e de integração com Pytest.
* Dockerização da aplicação para padronização de ambientes.
* Implementação de paginação e filtros avançados nas listagens.
* Transição de API Key para autenticação OAuth2 com JWT.

---

## Contato

**Bruna Rocha**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bruna-rocha-40a90b320/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/brunaroch-alt)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:brunaprbispo@hotmail.com)

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.