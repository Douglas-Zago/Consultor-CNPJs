# teste_final.py
# Um arquivo único para testar a interface de forma isolada.

import time
import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from threading import Thread

# SIMULAÇÃO DO PROCESSO (não depende de outros arquivos)
def processo_simulado(progress_callback):
    total_simulado = 10
    contadores = {
        "Desenvolvedor": 0, "NaoDesenvolvedor": 0,
        "JaConsultado": 0, "NaoEncontrado": 0
    }
    categorias = list(contadores.keys())

    for i in range(total_simulado):
        # Chama o callback para atualizar a UI
        if progress_callback:
            progress_callback(i + 1, total_simulado, "Simulando...", contadores)
        
        # Simula o trabalho pesado (como uma chamada de API)
        time.sleep(1) 
        
        # Simula a classificação de um CNPJ
        categoria_sorteada = random.choice(categorias)
        contadores[categoria_sorteada] += 1
        
    return contadores

# CLASSE DA INTERFACE (código que já conhecemos)
class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("TESTE FINAL DA INTERFACE")
        self.geometry("700x450") # Um pouco menor para o teste
        self.resizable(False, False)
        self.start_time = 0
        self.mensagens_status = [
            "Carregando...", "Consultando a base de dados...", "Validando informações...",
            "Falta pouco!", "Organizando os resultados...", "Quase lá...", "Já está acabando!"
        ]
        self.mensagem_idx = 0
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)
        ttk.Label(main_frame, text="Teste de Interface Isolada", font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))
        
        self.btn_iniciar = ttk.Button(main_frame, text="Iniciar Simulação", command=self.iniciar_processamento, style="success.TButton", bootstyle=SUCCESS)
        self.btn_iniciar.pack(pady=10, ipady=5, fill=X)

        self.progress = ttk.Progressbar(main_frame, style="success.Striped.TProgressbar", bootstyle=SUCCESS, mode="determinate")
        self.progress.pack(fill=X, pady=(20, 5))
        
        self.status_label = ttk.Label(main_frame, text="Clique em 'Iniciar Simulação'", font=("Segoe UI", 10))
        self.status_label.pack(pady=(0, 10))

        # Cards de contadores
        contadores_frame = ttk.Frame(main_frame)
        contadores_frame.pack(fill=X, expand=YES, pady=10)
        contadores_frame.columnconfigure((0, 1, 2, 3), weight=1)
        self.vars = {
            "Desenvolvedor": ttk.StringVar(value="0"), "NaoDesenvolvedor": ttk.StringVar(value="0"),
            "JaConsultado": ttk.StringVar(value="0"), "NaoEncontrado": ttk.StringVar(value="0"),
        }
        self.criar_card(contadores_frame, "Desenvolvedores", self.vars["Desenvolvedor"], "success").grid(row=0, column=0, padx=5, sticky="ew")
        self.criar_card(contadores_frame, "Não Devs", self.vars["NaoDesenvolvedor"], "info").grid(row=0, column=1, padx=5, sticky="ew")
        self.criar_card(contadores_frame, "Consultados", self.vars["JaConsultado"], "warning").grid(row=0, column=2, padx=5, sticky="ew")
        self.criar_card(contadores_frame, "Não Encontrados", self.vars["NaoEncontrado"], "secondary").grid(row=0, column=3, padx=5, sticky="ew")

    def criar_card(self, parent, titulo, var_texto, bootstyle):
        card = ttk.Frame(parent, borderwidth=1, relief="solid", padding=10, bootstyle=bootstyle)
        ttk.Label(card, text=titulo, font=("Segoe UI", 10, "bold"), bootstyle=(bootstyle, INVERSE)).pack()
        ttk.Label(card, textvariable=var_texto, font=("Segoe UI", 16, "bold"), bootstyle=(bootstyle, INVERSE)).pack(pady=5)
        return card

    def iniciar_processamento(self):
        self.btn_iniciar.config(state="disabled")
        self.progress["value"] = 0
        for var in self.vars.values(): var.set("0")
        self.status_label.config(text="Iniciando...")
        self.start_time = time.time()
        self.mensagem_idx = 0
        thread = Thread(target=self.rodar_processamento, daemon=True)
        thread.start()

    def rodar_processamento(self):
        resultados_finais = processo_simulado(self.atualizar_progresso)
        self.after(0, self.finalizar_processamento, resultados_finais)

    def atualizar_progresso(self, atual, total, status_msg, totais_parciais):
        self.after(0, self._safe_update_ui, atual, total, status_msg, totais_parciais)

    def _safe_update_ui(self, atual, total, status_msg, totais_parciais):
        if total > 0: self.progress["value"] = (atual / total) * 100
        for key, var in self.vars.items():
            var.set(str(totais_parciais.get(key, 0)))

        eta_str = ""
        elapsed_time = time.time() - self.start_time
        if atual > 0 and elapsed_time > 0:
            time_per_item = elapsed_time / atual
            remaining_items = total - atual
            remaining_time = remaining_items * time_per_item
            mins, secs = divmod(remaining_time, 60)
            eta_str = f" | ETA: {int(mins):02d}:{int(secs):02d}"
        
        mensagem_ciclica = self.mensagens_status[self.mensagem_idx]
        self.mensagem_idx = (self.mensagem_idx + 1) % len(self.mensagens_status)
        status_final = f"{mensagem_ciclica} ({atual} de {total}){eta_str}"
        self.status_label.config(text=status_final)

    def finalizar_processamento(self, resultados_finais):
        self.btn_iniciar.config(state="normal")
        texto_final = f"Simulação concluída! {sum(resultados_finais.values())} registros simulados."
        self.status_label.config(text=texto_final)
        self.progress["value"] = 100

# Ponto de entrada para executar este arquivo diretamente
if __name__ == "__main__":
    app = App()
    app.mainloop()