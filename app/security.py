import os
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise RuntimeError('ERRO: A variável de ambiente API_KEY não foi definida!')

API_KEY_NAME = 'X-API-KEY'

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def validar_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Acesso negado: Cabeçalho X-API-KEY ausente.',
        )
    
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Acesso negado: Chave de API inválida.',
        )
    
    return api_key