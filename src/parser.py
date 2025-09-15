# src/parser.py
"""
Módulo para analisar e formatar os dados brutos retornados pela API.
"""


def classificar_empresa(data: dict):
    """
    Extrai informações relevantes do dicionário da API e classifica a empresa.

    Args:
        data (dict): O dicionário JSON retornado pela API.

    Returns:
        tuple: Uma tupla contendo a categoria (str) e um dicionário com os dados formatados.
               Retorna ("NaoEncontrado", None) se os dados de entrada forem inválidos.
    """
    if not data:
        return "NaoEncontrado", None

    # Extrai os dados de forma segura, usando .get() para evitar erros se uma chave não existir.
    cnpj = data.get("taxId", "")
    nome = data.get("alias") or data.get("company", {}).get("name", "")

    # Concatena todos os telefones encontrados em uma única string.
    telefones_encontrados = []
    for tel in data.get("phones", []):
        area, numero = tel.get("area", ""), tel.get("number", "")
        if area and numero:
            telefones_encontrados.append(f"({area}) {numero}")
    telefone_final = " / ".join(telefones_encontrados)

    # Concatena todos os e-mails encontrados em uma única string.
    emails_encontrados = []
    for email in data.get("emails", []):
        endereco = email.get("address", "")
        if endereco:
            emails_encontrados.append(endereco)
    email_final = " / ".join(emails_encontrados)

    # Classifica como "Desenvolvedor" se a palavra "desenvolvimento" aparecer em qualquer atividade (CNAE).
    cnae_principal = data.get("mainActivity", {}).get("text", "")
    todas_atividades = [cnae_principal] + [
        act.get("text", "") for act in data.get("sideActivities", [])
    ]
    is_dev = any("desenvolvimento" in str(c).lower() for c in todas_atividades)

    registro = {
        "cnpj": cnpj,
        "nome": nome,
        "telefone": telefone_final,
        "email": email_final,
    }

    categoria = "Desenvolvedor" if is_dev else "NaoDesenvolvedor"
    return categoria, registro
