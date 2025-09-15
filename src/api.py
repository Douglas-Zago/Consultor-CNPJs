# src/api.py
"""
Módulo responsável pela comunicação com a API externa CNPJá.
"""
import requests
from requests.exceptions import RequestException, JSONDecodeError


def consulta_cnpj(cnpj: str):
    """
    Consulta um CNPJ na API CNPJá Office e retorna os dados em formato JSON.

    Args:
        cnpj (str): O número do CNPJ a ser consultado, apenas dígitos.

    Returns:
        dict or None: Um dicionário com os dados da empresa se a consulta for bem-sucedida,
                      caso contrário, retorna None.
    """
    url = f"https://open.cnpja.com/office/{cnpj}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            # Tenta decodificar o JSON. Se a resposta não for um JSON válido, falha graciosamente.
            return r.json()
        else:
            print(f"AVISO: API retornou status {r.status_code} para o CNPJ {cnpj}")
            return None
    except JSONDecodeError:
        # Captura o erro caso a resposta da API não seja um JSON válido (ex: um erro em HTML).
        print(
            f"ERRO CRÍTICO: A resposta da API para o CNPJ {cnpj} não foi um JSON válido."
        )
        return None
    except RequestException as e:
        # Captura erros de conexão, timeout, etc.
        print(f"ERRO DE CONEXÃO: Falha ao consultar o CNPJ {cnpj}. Erro: {e}")
        return None
