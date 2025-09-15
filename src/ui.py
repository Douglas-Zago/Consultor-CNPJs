# src/ui.py
"""
Módulo responsável pela criação e gerenciamento da interface gráfica (GUI) da aplicação.
"""
import os
import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from threading import Thread
from tkinter import filedialog, messagebox
from .main import processar_arquivo


class App(ttk.Window):
    """A classe principal da aplicação, que gerencia todos os widgets e eventos da interface."""

    def __init__(self):
        super().__init__(themename="superhero")

        self.title("Consulta e Classificação de CNPJs")
        self.geometry("700x550")
        self.resizable(False, False)

        self.arquivo_path = ""
        self.start_time = 0

        self.create_widgets()

    def create_widgets(self):
        """Cria e posiciona todos os elementos visuais (widgets) na janela."""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        ttk.Label(
            main_frame, text="Processador de CNPJs", font=("Segoe UI", 16, "bold")
        ).pack(pady=(0, 10))

        self.btn_selecionar = ttk.Button(
            main_frame,
            text="1. Escolher Arquivo (.txt)",
            command=self.escolher_arquivo,
            style="primary.TButton",
            bootstyle=PRIMARY,
        )
        self.btn_selecionar.pack(pady=10, ipady=5, fill=X)

        self.btn_iniciar = ttk.Button(
            main_frame,
            text="2. Iniciar Processamento",
            command=self.iniciar_processamento,
            style="success.TButton",
            state="disabled",
            bootstyle=SUCCESS,
        )
        self.btn_iniciar.pack(pady=5, ipady=5, fill=X)

        self.arquivo_var = ttk.StringVar(value="Nenhum arquivo selecionado")
        ttk.Label(main_frame, textvariable=self.arquivo_var, font=("Segoe UI", 9)).pack(
            pady=(0, 20)
        )

        contadores_frame = ttk.Frame(main_frame)
        contadores_frame.pack(fill=BOTH, expand=YES)
        contadores_frame.columnconfigure((0, 1), weight=1)
        contadores_frame.rowconfigure((0, 1), weight=1)

        self.vars = {
            "Desenvolvedor": ttk.StringVar(value="0"),
            "NaoDesenvolvedor": ttk.StringVar(value="0"),
            "JaConsultado": ttk.StringVar(value="0"),
            "NaoEncontrado": ttk.StringVar(value="0"),
        }
        self.criar_card(
            contadores_frame, "Desenvolvedores", self.vars["Desenvolvedor"], "success"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.criar_card(
            contadores_frame,
            "Não Desenvolvedores",
            self.vars["NaoDesenvolvedor"],
            "info",
        ).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.criar_card(
            contadores_frame, "Já Consultados", self.vars["JaConsultado"], "warning"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.criar_card(
            contadores_frame, "Não Encontrados", self.vars["NaoEncontrado"], "secondary"
        ).grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.progress = ttk.Progressbar(
            main_frame,
            style="success.Striped.TProgressbar",
            bootstyle=SUCCESS,
            mode="determinate",
        )
        self.progress.pack(fill=X, pady=(20, 5))

        self.status_label = ttk.Label(
            main_frame, text="Aguardando arquivo...", font=("Segoe UI", 9)
        )
        self.status_label.pack(pady=(0, 10))

        self.fechar_var = ttk.BooleanVar(value=False)
        ttk.Checkbutton(
            main_frame,
            text="Fechar automaticamente ao concluir",
            variable=self.fechar_var,
            bootstyle="round-toggle",
        ).pack(pady=10)

    def criar_card(self, parent, titulo, var_texto, bootstyle):
        """Cria um card de exibição para os contadores."""
        card = ttk.Frame(
            parent, borderwidth=1, relief="solid", padding=20, bootstyle=bootstyle
        )
        ttk.Label(
            card,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            bootstyle=(bootstyle, INVERSE),
        ).pack()
        ttk.Label(
            card,
            textvariable=var_texto,
            font=("Segoe UI", 22, "bold"),
            bootstyle=(bootstyle, INVERSE),
        ).pack(pady=(10, 0))
        return card

    def escolher_arquivo(self):
        """Abre uma janela para o usuário selecionar o arquivo de CNPJs."""
        path = filedialog.askopenfilename(
            title="Selecione um arquivo TXT com CNPJs",
            filetypes=[("Arquivos de Texto", "*.txt")],
        )
        if not path:
            return
        self.arquivo_path = path
        self.arquivo_var.set(f"Arquivo: {os.path.basename(path)}")
        self.btn_iniciar.config(state="normal")

    def iniciar_processamento(self):
        """Inicia a lógica de processamento em uma thread separada para não travar a interface."""
        if not self.arquivo_path:
            messagebox.showwarning("Aviso", "Nenhum arquivo foi selecionado.")
            return

        # Reseta a interface para um novo processamento
        self.btn_selecionar.config(state="disabled")
        self.btn_iniciar.config(state="disabled")
        self.progress["value"] = 0
        for var in self.vars.values():
            var.set("0")
        self.status_label.config(text="Iniciando...")
        self.start_time = time.time()

        # Cria e inicia a thread de trabalho
        thread = Thread(target=self.rodar_processamento, daemon=True)
        thread.start()

    def rodar_processamento(self):
        """Função executada pela thread de trabalho. Chama a lógica principal."""
        resultados_finais = processar_arquivo(
            self.arquivo_path, self.atualizar_progresso
        )
        # Agenda a função de finalização para ser executada na thread principal
        self.after(0, self.finalizar_processamento, resultados_finais)

    def atualizar_progresso(self, atual, total, status_msg, totais_parciais):
        """Callback que a lógica principal chama. Agenda a atualização da UI."""
        self.after(0, self._safe_update_ui, atual, total, status_msg, totais_parciais)

    def _safe_update_ui(self, atual, total, status_msg, totais_parciais):
        """Atualiza de forma segura os widgets da interface com o progresso atual."""
        if total > 0:
            self.progress["value"] = (atual / total) * 100
        for key, var in self.vars.items():
            var.set(str(totais_parciais.get(key, 0)))

        # Monta a string de status simplificada
        status_final = f"Processando: {atual} de {total}"
        self.status_label.config(text=status_final)

    def finalizar_processamento(self, resultados_finais):
        """Executa na thread principal quando o processo termina, atualizando a UI para o estado final."""
        if resultados_finais is None:  # Ocorreu um erro no processamento
            self.btn_selecionar.config(state="normal")
            self.btn_iniciar.config(state="disabled")
            self.status_label.config(text="Aguardando novo arquivo...")
            self.arquivo_var.set("Nenhum arquivo selecionado")
            self.progress["value"] = 0
            return

        for key, var in self.vars.items():
            var.set(str(resultados_finais.get(key, 0)))

        self.btn_selecionar.config(state="normal")
        self.btn_iniciar.config(state="disabled")
        texto_final = f"Processamento concluído! {sum(resultados_finais.values())} registros processados."
        self.status_label.config(text=texto_final)
        self.progress["value"] = 100

        messagebox.showinfo(
            "Sucesso",
            "Processamento concluído!\nResultados salvos como 'resultado_final.csv' na pasta 'data'.",
        )

        if self.fechar_var.get():
            self.destroy()


def criar_interface():
    """Função de ponto de entrada para iniciar a aplicação."""
    app = App()
    app.mainloop()
