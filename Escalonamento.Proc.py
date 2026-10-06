import tkinter as tk
from tkinter import ttk


def fcfs(processos):
    tempo = 0
    execucoes = []
    resultados = {}

    for processo in processos:
        inicio = tempo
        fim = tempo + processo["cpu"]

        execucoes.append({
            "nome": processo["nome"],
            "inicio": inicio,
            "fim": fim
        })

        tempo = fim

        resultados[processo["nome"]] = {
            "espera": fim - processo["cpu"],
            "turnaround": fim
        }

    return execucoes, resultados


def sjf(processos):
    fila = sorted(processos, key=lambda processo: processo["cpu"])

    tempo = 0
    execucoes = []
    resultados = {}

    for processo in fila:
        inicio = tempo
        fim = tempo + processo["cpu"]

        execucoes.append({
            "nome": processo["nome"],
            "inicio": inicio,
            "fim": fim
        })

        tempo = fim

        resultados[processo["nome"]] = {
            "espera": fim - processo["cpu"],
            "turnaround": fim
        }

    return execucoes, resultados


def prioridade(processos):
    fila = sorted(processos, key=lambda processo: processo["prioridade"])

    tempo = 0
    execucoes = []
    resultados = {}

    for processo in fila:
        inicio = tempo
        fim = tempo + processo["cpu"]

        execucoes.append({
            "nome": processo["nome"],
            "inicio": inicio,
            "fim": fim
        })

        tempo = fim

        resultados[processo["nome"]] = {
            "espera": fim - processo["cpu"],
            "turnaround": fim
        }

    return execucoes, resultados


def round_robin(processos, quantum=2):
    restantes = {}

    for processo in processos:
        restantes[processo["nome"]] = processo["cpu"]

    tempo = 0
    fila = processos.copy()

    execucoes = []
    resultados = {}

    while fila:
        processo = fila.pop(0)
        nome = processo["nome"]

        inicio = tempo
        executado = min(quantum, restantes[nome])

        tempo += executado
        restantes[nome] -= executado

        execucoes.append({
            "nome": nome,
            "inicio": inicio,
            "fim": tempo
        })

        if restantes[nome] == 0:
            resultados[nome] = {
                "espera": tempo - processo["cpu"],
                "turnaround": tempo
            }
        else:
            fila.append(processo)

    return execucoes, resultados


cenarios = {
    "Cenário 1": [
        {"nome": "P1", "cpu": 3, "prioridade": 1},
        {"nome": "P2", "cpu": 1, "prioridade": 1},
        {"nome": "P3", "cpu": 2, "prioridade": 1}
    ],

    "Cenário 2": [
        {"nome": "P1", "cpu": 8, "prioridade": 1},
        {"nome": "P2", "cpu": 2, "prioridade": 1},
        {"nome": "P3", "cpu": 1, "prioridade": 1}
    ],

    "Cenário 3": [
        {"nome": "P1", "cpu": 4, "prioridade": 3},
        {"nome": "P2", "cpu": 2, "prioridade": 1},
        {"nome": "P3", "cpu": 3, "prioridade": 2}
    ]
}


class Simulador:

    def __init__(self, janela):

        self.janela = janela

        self.janela.title("Simulador de Escalonamento")
        self.janela.geometry("1050x720")
        self.janela.minsize(900, 650)

        self.bg = "#09090d"
        self.card = "#111116"
        self.card2 = "#15151c"

        self.roxo = "#7c3aed"
        self.roxo_escuro = "#4c1d95"
        self.roxo_claro = "#a78bfa"

        self.texto = "#f5f3ff"
        self.texto_secundario = "#85838f"
        self.borda = "#24232d"

        self.janela.configure(bg=self.bg)

        self.algoritmos = {
            "FCFS": fcfs,
            "SJF": sjf,
            "Prioridade": prioridade,
            "Round Robin": round_robin
        }

        self.cenario_atual = "Cenário 1"
        self.algoritmo_atual = "FCFS"

        self.animando = False
        self.animacoes = []

        self.criar_estilo()
        self.criar_interface()

        self.executar(primeira_execucao=True)

    def criar_estilo(self):

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background=self.card,
            foreground=self.texto,
            fieldbackground=self.card,
            rowheight=42,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            background=self.card2,
            foreground=self.texto_secundario,
            borderwidth=0,
            font=("Segoe UI", 9, "bold"),
            padding=12
        )

        estilo.map(
            "Treeview",
            background=[
                ("selected", self.roxo_escuro)
            ],
            foreground=[
                ("selected", self.texto)
            ]
        )

        estilo.configure(
            "TCombobox",
            fieldbackground=self.card2,
            background=self.card2,
            foreground=self.texto,
            arrowcolor=self.roxo_claro,
            borderwidth=0
        )

    def criar_interface(self):

        topo = tk.Frame(
            self.janela,
            bg=self.bg
        )

        topo.pack(
            fill="x",
            padx=45,
            pady=(35, 20)
        )

        titulo = tk.Label(
            topo,
            text="Simulador de Escalonamento",
            font=("Segoe UI", 26, "bold"),
            bg=self.bg,
            fg=self.texto
        )

        titulo.pack(anchor="w")

        subtitulo = tk.Label(
            topo,
            text="Simulador de escalonamento de processos",
            font=("Segoe UI", 10),
            bg=self.bg,
            fg=self.texto_secundario
        )

        subtitulo.pack(
            anchor="w",
            pady=(4, 0)
        )

        controles = tk.Frame(
            self.janela,
            bg=self.card
        )

        controles.pack(
            fill="x",
            padx=45,
            pady=5
        )

        tk.Label(
            controles,
            text="CENÁRIO",
            font=("Segoe UI", 8, "bold"),
            bg=self.card,
            fg=self.texto_secundario
        ).pack(
            side="left",
            padx=(22, 8),
            pady=20
        )

        self.combo_cenario = ttk.Combobox(
            controles,
            values=list(cenarios.keys()),
            state="readonly",
            width=15,
            font=("Segoe UI", 10)
        )

        self.combo_cenario.set(self.cenario_atual)

        self.combo_cenario.pack(
            side="left",
            padx=5
        )

        self.combo_cenario.bind(
            "<<ComboboxSelected>>",
            self.mudar_cenario
        )

        tk.Label(
            controles,
            text="QUANTUM",
            font=("Segoe UI", 8, "bold"),
            bg=self.card,
            fg=self.texto_secundario
        ).pack(
            side="left",
            padx=(35, 8)
        )

        self.quantum = tk.Entry(
            controles,
            width=5,
            justify="center",
            bg=self.card2,
            fg=self.texto,
            insertbackground=self.roxo_claro,
            relief="flat",
            font=("Segoe UI", 10)
        )

        self.quantum.insert(0, "2")

        self.quantum.pack(
            side="left"
        )

        algoritmos = tk.Frame(
            self.janela,
            bg=self.bg
        )

        algoritmos.pack(
            fill="x",
            padx=45,
            pady=(25, 10)
        )

        tk.Label(
            algoritmos,
            text="ALGORITMO",
            font=("Segoe UI", 8, "bold"),
            bg=self.bg,
            fg=self.texto_secundario
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        botoes = tk.Frame(
            algoritmos,
            bg=self.bg
        )

        botoes.pack(anchor="w")

        self.botoes_algoritmos = {}

        for nome in self.algoritmos:

            botao = tk.Button(
                botoes,
                text=nome,
                command=lambda n=nome: self.selecionar_algoritmo(n),
                font=("Segoe UI", 9, "bold"),
                bg=self.card,
                fg=self.texto_secundario,
                activebackground=self.roxo_escuro,
                activeforeground=self.texto,
                relief="flat",
                bd=0,
                padx=22,
                pady=10,
                cursor="hand2"
            )

            botao.pack(
                side="left",
                padx=(0, 8)
            )

            botao.bind(
                "<ButtonPress-1>",
                lambda e, b=botao: self.botao_pressionado(b)
            )

            botao.bind(
                "<ButtonRelease-1>",
                lambda e, b=botao: self.botao_soltado(b)
            )

            self.botoes_algoritmos[nome] = botao

        informacao = tk.Frame(
            self.janela,
            bg=self.bg
        )

        informacao.pack(
            fill="x",
            padx=45,
            pady=(20, 12)
        )

        self.label_algoritmo = tk.Label(
            informacao,
            text="FCFS",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg,
            fg=self.roxo_claro
        )

        self.label_algoritmo.pack(
            side="left"
        )

        self.label_cenario = tk.Label(
            informacao,
            text="",
            font=("Segoe UI", 9),
            bg=self.bg,
            fg=self.texto_secundario
        )

        self.label_cenario.pack(
            side="left",
            padx=15
        )

        tabela_frame = tk.Frame(
            self.janela,
            bg=self.card
        )

        tabela_frame.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=5
        )

        colunas = (
            "processo",
            "cpu",
            "prioridade",
            "espera",
            "turnaround"
        )

        self.tabela = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings"
        )

        nomes_colunas = {
            "processo": "PROCESSO",
            "cpu": "CPU",
            "prioridade": "PRIORIDADE",
            "espera": "ESPERA",
            "turnaround": "TURNAROUND"
        }

        for coluna in colunas:

            self.tabela.heading(
                coluna,
                text=nomes_colunas[coluna]
            )

            self.tabela.column(
                coluna,
                anchor="center",
                width=150
            )

        self.tabela.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1
        )

        indicadores = tk.Frame(
            self.janela,
            bg=self.bg
        )

        indicadores.pack(
            fill="x",
            padx=45,
            pady=(15, 5)
        )

        self.label_espera = self.criar_indicador(
            indicadores,
            "ESPERA MÉDIA"
        )

        self.label_turnaround = self.criar_indicador(
            indicadores,
            "TURNAROUND MÉDIO"
        )

        timeline = tk.Frame(
            self.janela,
            bg=self.bg
        )

        timeline.pack(
            fill="x",
            padx=45,
            pady=(15, 25)
        )

        tk.Label(
            timeline,
            text="LINHA DO TEMPO",
            font=("Segoe UI", 8, "bold"),
            bg=self.bg,
            fg=self.texto_secundario
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        self.canvas = tk.Canvas(
            timeline,
            height=65,
            bg=self.card,
            highlightthickness=0
        )

        self.canvas.pack(
            fill="x"
        )

    def criar_indicador(self, pai, titulo):

        frame = tk.Frame(
            pai,
            bg=self.card
        )

        frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )

        tk.Label(
            frame,
            text=titulo,
            font=("Segoe UI", 8, "bold"),
            bg=self.card,
            fg=self.texto_secundario
        ).pack(
            anchor="w",
            padx=18,
            pady=(12, 2)
        )

        valor = tk.Label(
            frame,
            text="0.00",
            font=("Segoe UI", 17, "bold"),
            bg=self.card,
            fg=self.texto
        )

        valor.pack(
            anchor="w",
            padx=18,
            pady=(0, 12)
        )

        return valor

    def cancelar_animacoes(self):

        for animacao in self.animacoes:

            try:
                self.janela.after_cancel(animacao)
            except:
                pass

        self.animacoes.clear()
        self.animando = False

    def agendar(self, funcao, tempo):

        identificador = self.janela.after(
            tempo,
            funcao
        )

        self.animacoes.append(
            identificador
        )

    def mudar_cenario(self, evento=None):

        self.cenario_atual = self.combo_cenario.get()

        self.executar()

    def selecionar_algoritmo(self, algoritmo):

        if self.algoritmo_atual == algoritmo and not self.animando:
            return

        self.algoritmo_atual = algoritmo

        self.executar()

    def botao_pressionado(self, botao):

        if botao["state"] != "disabled":

            botao.config(
                relief="sunken",
                bg=self.roxo_escuro
            )

    def botao_soltado(self, botao):

        botao.config(
            relief="flat"
        )

        self.atualizar_botoes()

    def executar(self, primeira_execucao=False):

        self.cancelar_animacoes()

        processos = cenarios[self.cenario_atual]

        if self.algoritmo_atual == "Round Robin":

            try:
                quantum = int(self.quantum.get())

                if quantum <= 0:
                    quantum = 2

            except ValueError:
                quantum = 2

            execucoes, resultados = round_robin(
                processos,
                quantum
            )

        else:

            funcao = self.algoritmos[
                self.algoritmo_atual
            ]

            execucoes, resultados = funcao(
                processos
            )

        self.atualizar_botoes()

        self.label_algoritmo.config(
            text=self.algoritmo_atual
        )

        self.label_cenario.config(
            text=self.cenario_atual
        )

        if primeira_execucao:

            self.atualizar_tabela(
                processos,
                resultados
            )

            self.atualizar_medias(
                processos,
                resultados
            )

            self.janela.after(
                100,
                lambda: self.desenhar_linha_tempo(execucoes)
            )

            return

        self.animando = True

        self.limpar_resultados()

        self.agendar(
            lambda: self.animar_tabela(
                processos,
                resultados
            ),
            180
        )

        self.agendar(
            lambda: self.animar_medias(
                processos,
                resultados
            ),
            350
        )

        self.agendar(
            lambda: self.animar_timeline(
                execucoes
            ),
            500
        )

        self.agendar(
            self.finalizar_animacao,
            1200
        )

    def finalizar_animacao(self):

        self.animando = False
        self.atualizar_botoes()

    def limpar_resultados(self):

        for item in self.tabela.get_children():

            self.tabela.delete(item)

        self.label_espera.config(
            text="0.00"
        )

        self.label_turnaround.config(
            text="0.00"
        )

        self.canvas.delete("all")

    def atualizar_botoes(self):

        for nome, botao in self.botoes_algoritmos.items():

            if nome == self.algoritmo_atual:

                botao.config(
                    bg=self.roxo_escuro,
                    fg=self.texto
                )

            else:

                botao.config(
                    bg=self.card,
                    fg=self.texto_secundario
                )

    def atualizar_tabela(
        self,
        processos,
        resultados
    ):

        for item in self.tabela.get_children():

            self.tabela.delete(item)

        for processo in processos:

            nome = processo["nome"]

            self.tabela.insert(
                "",
                "end",
                values=(
                    nome,
                    processo["cpu"],
                    processo["prioridade"],
                    resultados[nome]["espera"],
                    resultados[nome]["turnaround"]
                )
            )

    def animar_tabela(
        self,
        processos,
        resultados,
        indice=0
    ):

        if indice >= len(processos):
            return

        processo = processos[indice]
        nome = processo["nome"]

        self.tabela.insert(
            "",
            "end",
            values=(
                nome,
                processo["cpu"],
                processo["prioridade"],
                "calculando...",
                "calculando..."
            )
        )

        item = self.tabela.get_children()[-1]

        self.animar_valor_tabela(
            item,
            resultados[nome]["espera"],
            resultados[nome]["turnaround"],
            0
        )

        self.agendar(
            lambda: self.animar_tabela(
                processos,
                resultados,
                indice + 1
            ),
            180
        )

    def animar_valor_tabela(
        self,
        item,
        espera_final,
        turnaround_final,
        valor
    ):

        if not self.tabela.exists(item):
            return

        passo = 1

        espera = min(
            valor + passo,
            espera_final
        )

        turnaround = min(
            valor + passo,
            turnaround_final
        )

        valores = self.tabela.item(
            item,
            "values"
        )

        if len(valores) >= 5:

            self.tabela.item(
                item,
                values=(
                    valores[0],
                    valores[1],
                    valores[2],
                    espera,
                    turnaround
                )
            )

        if espera < espera_final or turnaround < turnaround_final:

            self.agendar(
                lambda: self.animar_valor_tabela(
                    item,
                    espera_final,
                    turnaround_final,
                    valor + 1
                ),
                45
            )

    def atualizar_medias(
        self,
        processos,
        resultados
    ):

        soma_espera = 0
        soma_turnaround = 0

        for processo in processos:

            nome = processo["nome"]

            soma_espera += resultados[
                nome
            ]["espera"]

            soma_turnaround += resultados[
                nome
            ]["turnaround"]

        media_espera = soma_espera / len(processos)
        media_turnaround = soma_turnaround / len(processos)

        self.label_espera.config(
            text=f"{media_espera:.2f}"
        )

        self.label_turnaround.config(
            text=f"{media_turnaround:.2f}"
        )

    def animar_medias(
        self,
        processos,
        resultados
    ):

        soma_espera = 0
        soma_turnaround = 0

        for processo in processos:

            nome = processo["nome"]

            soma_espera += resultados[
                nome
            ]["espera"]

            soma_turnaround += resultados[
                nome
            ]["turnaround"]

        media_espera = soma_espera / len(processos)
        media_turnaround = soma_turnaround / len(processos)

        self.contador(
            self.label_espera,
            0,
            media_espera,
            0
        )

        self.contador(
            self.label_turnaround,
            0,
            media_turnaround,
            0
        )

    def contador(
        self,
        label,
        atual,
        destino,
        passo
    ):

        if atual >= destino:

            label.config(
                text=f"{destino:.2f}"
            )

            return

        diferenca = destino - atual

        incremento = max(
            diferenca / 8,
            0.05
        )

        novo_valor = min(
            atual + incremento,
            destino
        )

        label.config(
            text=f"{novo_valor:.2f}"
        )

        self.agendar(
            lambda: self.contador(
                label,
                novo_valor,
                destino,
                passo + 1
            ),
            45
        )

    def desenhar_linha_tempo(
        self,
        execucoes
    ):

        self.canvas.delete("all")

        if not execucoes:
            return

        fim_total = execucoes[-1]["fim"]

        largura = self.canvas.winfo_width()

        if largura <= 1:
            largura = 900

        margem = 20
        largura_util = largura - margem * 2

        cores = {
            "P1": "#5b21b6",
            "P2": "#7c3aed",
            "P3": "#9333ea",
            "P4": "#a855f7"
        }

        for execucao in execucoes:

            inicio = execucao["inicio"]
            fim = execucao["fim"]
            nome = execucao["nome"]

            x1 = (
                margem +
                inicio / fim_total *
                largura_util
            )

            x2 = (
                margem +
                fim / fim_total *
                largura_util
            )

            cor = cores.get(
                nome,
                self.roxo
            )

            self.canvas.create_rectangle(
                x1,
                15,
                x2,
                48,
                fill=cor,
                outline=""
            )

            if x2 - x1 > 25:

                self.canvas.create_text(
                    (x1 + x2) / 2,
                    31,
                    text=nome,
                    fill=self.texto,
                    font=("Segoe UI", 9, "bold")
                )

            self.canvas.create_text(
                x1,
                56,
                text=str(inicio),
                fill=self.texto_secundario,
                font=("Segoe UI", 8)
            )

        self.canvas.create_text(
            margem + largura_util,
            56,
            text=str(fim_total),
            fill=self.texto_secundario,
            font=("Segoe UI", 8)
        )

    def animar_timeline(
        self,
        execucoes
    ):

        self.canvas.delete("all")

        if not execucoes:
            return

        fim_total = execucoes[-1]["fim"]

        largura = self.canvas.winfo_width()

        if largura <= 1:
            largura = 900

        margem = 20
        largura_util = largura - margem * 2

        cores = {
            "P1": "#5b21b6",
            "P2": "#7c3aed",
            "P3": "#9333ea",
            "P4": "#a855f7"
        }

        self.animar_bloco_timeline(
            execucoes,
            fim_total,
            largura_util,
            margem,
            cores,
            0
        )

    def animar_bloco_timeline(
        self,
        execucoes,
        fim_total,
        largura_util,
        margem,
        cores,
        indice
    ):

        if indice >= len(execucoes):
            self.desenhar_marcadores(
                execucoes,
                fim_total,
                largura_util,
                margem
            )

            return

        execucao = execucoes[indice]

        inicio = execucao["inicio"]
        fim = execucao["fim"]
        nome = execucao["nome"]

        x1 = (
            margem +
            inicio / fim_total *
            largura_util
        )

        x2 = (
            margem +
            fim / fim_total *
            largura_util
        )

        cor = cores.get(
            nome,
            self.roxo
        )

        self.canvas.create_rectangle(
            x1,
            15,
            x1,
            48,
            fill=cor,
            outline=""
        )

        passos = 12

        def expandir(passo):

            progresso = passo / passos
            atual_x2 = x1 + (x2 - x1) * progresso

            self.canvas.coords(
                self.canvas.find_all()[-1],
                x1,
                15,
                atual_x2,
                48
            )

            if passo < passos:

                self.agendar(
                    lambda: expandir(passo + 1),
                    20
                )

            else:

                if x2 - x1 > 25:

                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        31,
                        text=nome,
                        fill=self.texto,
                        font=("Segoe UI", 9, "bold")
                    )

                self.agendar(
                    lambda: self.animar_bloco_timeline(
                        execucoes,
                        fim_total,
                        largura_util,
                        margem,
                        cores,
                        indice + 1
                    ),
                    80
                )

        expandir(1)

    def desenhar_marcadores(
        self,
        execucoes,
        fim_total,
        largura_util,
        margem
    ):

        for execucao in execucoes:

            inicio = execucao["inicio"]

            x1 = (
                margem +
                inicio / fim_total *
                largura_util
            )

            self.canvas.create_text(
                x1,
                56,
                text=str(inicio),
                fill=self.texto_secundario,
                font=("Segoe UI", 8)
            )

        self.canvas.create_text(
            margem + largura_util,
            56,
            text=str(fim_total),
            fill=self.texto_secundario,
            font=("Segoe UI", 8)
        )


janela = tk.Tk()

app = Simulador(janela)

janela.mainloop()