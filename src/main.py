# src/main.py
"""
Módulo principal da lógica de negócio. Orquestra o processamento do arquivo de CNPJs.
"""
import os
import time
import csv
from tkinter import messagebox
from .api import consulta_cnpj
from .parser import classificar_empresa


def processar_arquivo(path: str, progress_callback=None):
    """
    Lê um arquivo de CNPJs, processa cada um, e salva os resultados em um CSV.

    Args:
        path (str): O caminho para o arquivo de texto contendo os CNPJs.
        progress_callback (function, optional): Uma função para reportar o progresso para a UI.

    Returns:
        dict or None: Um dicionário com os contadores finais do processo,
                      ou None se ocorrer um erro que impeça o processamento.
    """
    os.makedirs("data", exist_ok=True)
    JA_CONSULTADOS_FILE = "data/ja_consultados.txt"

    try:
        with open(JA_CONSULTADOS_FILE, "r", encoding="utf-8") as f:
            ja_consultados = {line.strip() for line in f}
    except FileNotFoundError:
        ja_consultados = set()

    try:
        with open(path, "r", encoding="utf-8") as f_in:
            cnpjs_a_processar = [line.strip() for line in f_in if line.strip()]
    except Exception as e:
        messagebox.showerror(
            "Erro de Leitura", f"Não foi possível ler o arquivo.\n\nErro: {e}"
        )
        return None

    if not cnpjs_a_processar:
        messagebox.showerror(
            "Erro", "O arquivo selecionado está vazio ou não contém CNPJs válidos."
        )
        return None

    todos_os_resultados = []
    total_cnpjs = len(cnpjs_a_processar)

    contadores = {
        "Desenvolvedor": 0,
        "NaoDesenvolvedor": 0,
        "JaConsultado": 0,
        "NaoEncontrado": 0,
    }

    for i, cnpj_original in enumerate(cnpjs_a_processar):
        # Envolve a lógica de cada CNPJ em um try/except para garantir que,
        # se um der erro, o processo continue com os próximos.
        try:
            cnpj = "".join(filter(str.isdigit, cnpj_original))
            if not cnpj:
                continue

            # Reporta o progresso para a interface antes de iniciar o trabalho.
            if progress_callback:
                progress_callback(
                    i + 1, total_cnpjs, f"Consultando {cnpj}...", contadores
                )

            status_atual = ""
            if cnpj in ja_consultados:
                status_atual = "JaConsultado"
                todos_os_resultados.append(
                    {
                        "cnpj": cnpj,
                        "nome": "",
                        "telefone": "",
                        "email": "",
                        "status": status_atual,
                    }
                )
            else:
                data = consulta_cnpj(cnpj)
                categoria, registro_raw = classificar_empresa(data)

                # Valida se os dados essenciais (CNPJ e um contato) foram encontrados.
                if (
                    registro_raw
                    and registro_raw.get("cnpj")
                    and (registro_raw.get("telefone") or registro_raw.get("email"))
                ):
                    status_atual = categoria
                    registro_raw["status"] = status_atual
                    todos_os_resultados.append(registro_raw)
                else:
                    status_atual = "NaoEncontrado"
                    todos_os_resultados.append(
                        {
                            "cnpj": cnpj,
                            "nome": "",
                            "telefone": "",
                            "email": "",
                            "status": status_atual,
                        }
                    )

                # Salva o CNPJ na lista de já consultados e aguarda para não sobrecarregar a API.
                ja_consultados.add(cnpj)
                with open(JA_CONSULTADOS_FILE, "a", encoding="utf-8") as f_out:
                    f_out.write(cnpj + "\n")

                time.sleep(12)

            if status_atual:
                contadores[status_atual] += 1

        except Exception as e:
            print(
                f"ERRO INESPERADO no CNPJ {cnpj_original}. Pulando para o próximo. Erro: {e}"
            )
            contadores["NaoEncontrado"] += 1
            continue

    # Ordena os resultados para o CSV final de acordo com a prioridade definida.
    ordem_status = {
        "NaoDesenvolvedor": 1,
        "JaConsultado": 2,
        "Desenvolvedor": 3,
        "NaoEncontrado": 4,
    }
    todos_os_resultados.sort(key=lambda item: ordem_status.get(item["status"], 99))

    if todos_os_resultados:
        header = ["cnpj", "nome", "telefone", "email", "status"]
        try:
            with open(
                "data/resultado_final.csv", "w", newline="", encoding="utf-8-sig"
            ) as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                writer.writerows(todos_os_resultados)
        except Exception as e:
            messagebox.showerror(
                "Erro ao Salvar",
                f"Não foi possível salvar o arquivo de resultados.\n\nErro: {e}",
            )
            return None

    return contadores
