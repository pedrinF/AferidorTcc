import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import sqlite3
import datetime

# Conectar ao banco de dados (ou criar um novo)
conn = sqlite3.connect('historico_afericoes.db')
c = conn.cursor()

# Atualizar a estrutura do banco de dados
c.execute('''CREATE TABLE IF NOT EXISTS afericoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT,
    empresa TEXT,
    cnpj TEXT,
    endereco TEXT,
    cidade TEXT,
    nome_dispenser TEXT,
    numero_serie TEXT,
    numero_lacre TEXT,
    massa_especifica TEXT,
    lado_a TEXT,
    lado_b TEXT
)''')

# Adicionar as novas colunas ao banco existente, se não estiverem presentes
try:
    c.execute("ALTER TABLE afericoes ADD COLUMN lado_a TEXT")
    c.execute("ALTER TABLE afericoes ADD COLUMN lado_b TEXT")
    conn.commit()
except sqlite3.OperationalError:
    pass  # As colunas já existem, ignorar erro

def salvar_historico(empresa, cnpj, endereco, cidade, nome_dispenser, numero_serie, numero_lacre, massa_especifica, lado_a, lado_b):
    """Salvar os dados no banco de dados."""
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Converter listas de entradas em strings separadas por ";"
    lado_a_str = ";".join(",".join(entry.get() for entry in row[:4]) for row in lado_a)
    lado_b_str = ";".join(",".join(entry.get() for entry in row[:4]) for row in lado_b)

    # Inserir os dados no banco de dados
    c.execute(
        '''INSERT INTO afericoes (
            data_hora, empresa, cnpj, endereco, cidade,
            nome_dispenser, numero_serie, numero_lacre,
            massa_especifica, lado_a, lado_b
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (data_hora, empresa, cnpj, endereco, cidade,
         nome_dispenser, numero_serie, numero_lacre,
         massa_especifica, lado_a_str, lado_b_str)
    )
    conn.commit()

def gerar_pdf_afericao(dados, lado_a_dados, lado_b_dados, file_path):
    """Gerar um PDF com os dados recuperados com o layout igual a função gerar_pdf"""
    c = pdf_canvas.Canvas(file_path)
    largura, altura = 595.27, 841.89  # Dimensões padrão A4 em pontos (px)
    margem_esquerda = 50
    linha_atual = altura - 50

    c.setFont("Helvetica", 12)

    # Cabeçalho
    c.drawCentredString(largura / 2, linha_atual, "CF Serviços em Gás Natural")
    linha_atual -= 20
    c.drawCentredString(largura / 2, linha_atual, "CNPJ: 00.000.000/0001-00")
    linha_atual -= 15
    c.drawCentredString(largura / 2, linha_atual, "Endereço: Rua Fictícia, 123 - Cidade Exemplo")
    linha_atual -= 20
    c.drawCentredString(largura / 2, linha_atual, f"Data: {dados['data_hora']}")
    linha_atual -= 40

    # Título do relatório
    c.setFont("Helvetica", 14)
    c.drawCentredString(largura / 2, linha_atual, "Relatório de Aferição de Combustíveis")
    linha_atual -= 40

    # Informações da empresa
    c.setFont("Helvetica", 12)
    c.drawString(margem_esquerda, linha_atual, "Informações da Empresa:")
    linha_atual -= 20
    c.drawString(margem_esquerda, linha_atual, f"Empresa: {dados['empresa']}")
    linha_atual -= 20
    c.drawString(margem_esquerda, linha_atual, f"CNPJ: {dados['cnpj']}")
    linha_atual -= 20
    c.drawString(margem_esquerda, linha_atual, f"Endereço: {dados['endereco']}")
    linha_atual -= 20
    c.drawString(margem_esquerda, linha_atual, f"Cidade: {dados['cidade']}")
    linha_atual -= 40

    # Informações do dispenser
    c.drawString(margem_esquerda, linha_atual, "Informações do Dispenser:")
    linha_atual -= 20
    c.drawString(margem_esquerda, linha_atual, f"Nome do Dispenser: {dados['nome_dispenser']}")
    linha_atual -= 20
    c.drawString(margem_esquerda, linha_atual, f"Número de Série: {dados['numero_serie']}")
    linha_atual -= 20
    c.drawString(margem_esquerda, linha_atual, f"Número do Lacre: {dados['numero_lacre']}")
    linha_atual -= 20
    c.drawString(margem_esquerda, linha_atual, f"Massa Específica: {dados['massa_especifica']} kg/m³")
    linha_atual -= 40

    # Dados do lado A - Tabela
    c.drawString(margem_esquerda, linha_atual, f"Lado A - Número do Dispenser")
    linha_atual -= 20
    tabela_lado_a = [["Master (kg)", "Master (m³)", "Dispenser (m³)", "Erro (%)"]]
    for entrada in lado_a_dados.split(";"):
        tabela_lado_a.append(entrada.split(","))
    
    t = Table(tabela_lado_a)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black),
                           ('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                           ('FONTSIZE', (0, 0), (-1, -1), 12)]))
    t.wrapOn(c, largura, altura)
    t.drawOn(c, margem_esquerda, linha_atual - 100)
    linha_atual -= 100 + len(tabela_lado_a) * 20

    # Dados do lado B - Tabela
    c.drawString(margem_esquerda, linha_atual, f"Lado B - Número do Dispenser")
    linha_atual -= 20
    tabela_lado_b = [["Master (kg)", "Master (m³)", "Dispenser (m³)", "Erro (%)"]]
    for entrada in lado_b_dados.split(";"):
        tabela_lado_b.append(entrada.split(","))
    
    t = Table(tabela_lado_b)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black),
                           ('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
                           ('FONTSIZE', (0, 0), (-1, -1), 12)]))
    t.wrapOn(c, largura, altura)
    t.drawOn(c, margem_esquerda, linha_atual - 100)

    # Finalizar e salvar o PDF
    c.save()



# Função para carregar o histórico
def carregar_historico():
    c.execute("SELECT * FROM afericoes")
    return c.fetchall()



def calcular_erro(entry_master_padrao_kg, entry_master_padrao_m3, entry_display_dispenser, entry_erro_percent, massa_especifica_entry, entries_list, media_label):
    try:
        massa_especifica = float(massa_especifica_entry.get())
        master_padrao_kg = float(entry_master_padrao_kg.get())
        display_dispenser = float(entry_display_dispenser.get())
        
        # Calculo de Master padrão em m³ e do erro %
        master_padrao_m3 = master_padrao_kg / massa_especifica
        entry_master_padrao_m3.delete(0, tk.END)
        entry_master_padrao_m3.insert(0, f"{master_padrao_m3:.2f}")
        
        erro = ((display_dispenser - master_padrao_m3) / master_padrao_m3) * 100
        entry_erro_percent.delete(0, tk.END)
        entry_erro_percent.insert(0, f"{erro:.2f}")
        
        # Atualizando a média dos erros
        calcular_media_erros(entries_list, media_label)
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

def calcular_media_erros(entries_list, media_label):
    erros = []
    for row in entries_list:
        erro_str = row[3].get()
        if erro_str:
            try:
                erros.append(float(erro_str))
            except ValueError:
                continue
    if erros:
        media = sum(erros) / len(erros)
        media_label.config(text=f"{media:.2f}")
    else:
        media_label.config(text="0.00")

def adicionar_nova_linha(parent_frame, entries_list, lado, massa_especifica_entry, media_label):
    entry_master_padrao_kg = criar_entry(parent_frame, 15)
    entry_master_padrao_kg.grid(row=len(entries_list) + 1, column=1, padx=5, pady=5)
    
    entry_master_padrao_m3 = criar_entry(parent_frame, 15)
    entry_master_padrao_m3.grid(row=len(entries_list) + 1, column=2, padx=5, pady=5)
    
    entry_display_dispenser = criar_entry(parent_frame, 15)
    entry_display_dispenser.grid(row=len(entries_list) + 1, column=3, padx=5, pady=5)
    
    entry_erro_percent = criar_entry(parent_frame, 15)
    entry_erro_percent.grid(row=len(entries_list) + 1, column=4, padx=5, pady=5)
    
    btn_calcular = tk.Button(parent_frame, text="Calcular", 
                             command=lambda empkg=entry_master_padrao_kg, empm3=entry_master_padrao_m3, edd=entry_display_dispenser, eep=entry_erro_percent: calcular_erro(empkg, empm3, edd, eep, massa_especifica_entry, entries_list, media_label),
                             font=fonte_extra_bold, bg="#004AAD", fg="white")
    btn_calcular.grid(row=len(entries_list) + 1, column=5, padx=5, pady=5)
    
    entries_list.append((entry_master_padrao_kg, entry_master_padrao_m3, entry_display_dispenser, entry_erro_percent, btn_calcular))

def criar_secao_lado(titulo, inicio_y, lado, main_frame, entries_list, massa_especifica_entry):
    # Título da seção e campo de entrada para "Número Dispenser"
    label_titulo = tk.Label(main_frame, text=titulo, bg="#004AAD", fg="white", font=fonte_extra_bold)
    label_titulo.grid(row=inicio_y, column=2, sticky="w", padx=10)
    
    # Frame para as entradas da seção
    frame_lado = tk.Frame(main_frame, bg="#004AAD")
    frame_lado.grid(row=inicio_y + 1, column=2, sticky="w", padx=10, pady=10)
    
    # Labels das colunas
    labels = ["Master kg", "Master m³", "Dispenser m³", "Erro %"]
    for i, text in enumerate(labels):
        label = tk.Label(frame_lado, text=text, bg="#004AAD", fg="white", font=fonte_extra_bold)
        label.grid(row=0, column=i+1, padx=5, pady=5)

    # Campo de média de erro
    media_label = tk.Label(main_frame, text="0.00", bg="#004AAD", fg="white", font=fonte_extra_bold)

    # Adicionando linhas de entrada
    for _ in range(5):
        adicionar_nova_linha(frame_lado, entries_list, lado, massa_especifica_entry, media_label)
    
    # Campo para mostrar a média dos erros
    tk.Label(main_frame, text="Média Erro %:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=inicio_y + 2, column=2, sticky="w", padx=10)
    media_label.grid(row=inicio_y + 2, column=3, sticky="w")
    
    # Botão para adicionar novas linhas de entrada
    btn_adicionar = tk.Button(main_frame, text="Adicionar Linha", command=lambda: adicionar_nova_linha(frame_lado, entries_list, lado, massa_especifica_entry, media_label),
                              bg="blue", fg="white", font=fonte_extra_bold)
    btn_adicionar.grid(row=inicio_y, column=4, padx=10, pady=10)

def criar_entry(parent, largura):
    entry = tk.Entry(parent, bd=0, font=fonte_extra_bold, width=largura)
    return entry

def gerar_pdf(entry_empresa, entry_cnpj, entry_endereco, entry_cidade, entry_nome_dispenser,
              entry_numero_serie, entry_numero_lacre, massa_especifica_entry, 
              entry_numero_dispenser_a, entry_numero_dispenser_b, lado_a_entries, lado_b_entries):
    try:
        # Obter informações do posto
        empresa = entry_empresa.get()
        cnpj = entry_cnpj.get()
        endereco = entry_endereco.get()
        cidade = entry_cidade.get()
        nome_dispenser = entry_nome_dispenser.get()
        numero_serie = entry_numero_serie.get()
        numero_lacre = entry_numero_lacre.get()
        massa_especifica = massa_especifica_entry.get()
        numero_dispenser_a = entry_numero_dispenser_a.get()
        numero_dispenser_b = entry_numero_dispenser_b.get()

        salvar_historico(empresa, cnpj, endereco, cidade, nome_dispenser, numero_serie, numero_lacre, massa_especifica, lado_a_entries, lado_b_entries)
        

        # Solicitar local para salvar o PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                                 filetypes=[("PDF files", "*.pdf")],
                                                 title="Salvar Arquivo PDF")
        if not file_path:
            return  
        # Criar o PDF
        c = pdf_canvas.Canvas(file_path)
        largura, altura = 595.27, 841.89  # Dimensões padrão A4 em pontos (px)
        margem_esquerda = 50
        linha_atual = altura - 50

        # Configuração de fonte
        fonte_padrao = "Helvetica"
        c.setFont(fonte_padrao, 12)

        # Cabeçalho da empresa centralizado com Data
        c.drawCentredString(largura / 2, linha_atual, "CF Serviços em Gás Natural")
        linha_atual -= 20
        c.drawCentredString(largura / 2, linha_atual, "CNPJ: 00.000.000/0001-00")
        linha_atual -= 15
        c.drawCentredString(largura / 2, linha_atual, "Endereço: Rua Fictícia, 123 - Cidade Exemplo")
        linha_atual -= 20
        c.drawCentredString(largura / 2, linha_atual, f"Data: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        linha_atual -= 40

        # Título principal
        c.setFont(fonte_padrao, 14)
        c.drawCentredString(largura / 2, linha_atual, "Relatório de Aferição de Combustíveis")
        linha_atual -= 40

        # Informações da empresa
        c.setFont(fonte_padrao, 12)
        c.drawString(margem_esquerda, linha_atual, "Informações da Empresa:")
        linha_atual -= 20
        c.drawString(margem_esquerda, linha_atual, f"Empresa: {empresa}")
        linha_atual -= 20
        c.drawString(margem_esquerda, linha_atual, f"CNPJ: {cnpj}")
        linha_atual -= 20
        c.drawString(margem_esquerda, linha_atual, f"Endereço: {endereco}")
        linha_atual -= 20
        c.drawString(margem_esquerda, linha_atual, f"Cidade: {cidade}")
        linha_atual -= 40

        # Informações do dispenser
        c.drawString(margem_esquerda, linha_atual, "Informações do Dispenser:")
        linha_atual -= 20
        c.drawString(margem_esquerda, linha_atual, f"Nome do Dispenser: {nome_dispenser}")
        linha_atual -= 20
        c.drawString(margem_esquerda, linha_atual, f"Número de Série: {numero_serie}")
        linha_atual -= 20
        c.drawString(margem_esquerda, linha_atual, f"Número do Lacre: {numero_lacre}")
        linha_atual -= 20
        c.drawString(margem_esquerda, linha_atual, f"Massa Específica: {massa_especifica} kg/m³")
        linha_atual -= 40

        # Dados do lado A - Tabela
        c.drawString(margem_esquerda, linha_atual, f"Lado A - Número do Dispenser: {numero_dispenser_a}")
        linha_atual -= 20
        dados_lado_a = [["Master (kg)", "Master (m³)", "Dispenser (m³)", "Erro (%)"]]
        for row in lado_a_entries:
            valores = [entry.get() for entry in row[:4]]
            dados_lado_a.append(valores)

        # Criar e desenhar a tabela do lado A
        tabela_lado_a = Table(dados_lado_a)
        tabela_lado_a.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                           ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                           ('FONTNAME', (0, 0), (-1, -1), fonte_padrao),
                                           ('FONTSIZE', (0, 0), (-1, -1), 12)]))
        tabela_lado_a.wrapOn(c, largura, altura)
        tabela_lado_a.drawOn(c, margem_esquerda, linha_atual - 100)
        linha_atual -= 100 + len(dados_lado_a) * 20

        # Dados do lado B - Tabela
        c.drawString(margem_esquerda, linha_atual, f"Lado B - Número do Dispenser: {numero_dispenser_b}")
        linha_atual -= 20
        dados_lado_b = [["Master (kg)", "Master (m³)", "Dispenser (m³)", "Erro (%)"]]
        for row in lado_b_entries:
            valores = [entry.get() for entry in row[:4]]
            dados_lado_b.append(valores)

        # Criar e desenhar a tabela do lado B
        tabela_lado_b = Table(dados_lado_b)
        tabela_lado_b.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                           ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                           ('FONTNAME', (0, 0), (-1, -1), fonte_padrao),
                                           ('FONTSIZE', (0, 0), (-1, -1), 12)]))
        tabela_lado_b.wrapOn(c, largura, altura)
        tabela_lado_b.drawOn(c, margem_esquerda, linha_atual - 100)

        # Finalizar e salvar o PDF
        c.save()
        messagebox.showinfo("Sucesso", f"PDF salvo em {file_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Aferição")
        self.geometry("1200x700")
        self.frames = {}

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Configuração para expandir os frames no container
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Adiciona as telas (TelaInicial, TelaAfericao, TelaHistorico) ao dicionário frames
        for F in (TelaInicial, TelaAfericao, TelaHistorico):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostrar TelaInicial ao iniciar
        self.show_frame(TelaInicial)

    def show_frame(self, frame_class):
        """Eleva o frame especificado para o topo."""
        frame = self.frames[frame_class]
        frame.tkraise()  # Mostra o frame atual

class TelaInicial(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(bg="#004AAD")

        # Título
        label = tk.Label(self, text="METRONGAS V.1", bg="#004AAD", fg="white", font=("Arial", 18, "bold"))
        label.pack(pady=10)

        # Botão "Nova Aferição"
        botao_nova_afericao = tk.Button(self, text="Nova Aferição", font=("Arial", 14), bg="green", fg="white", 
                                        command=lambda: controller.show_frame(TelaAfericao))
        botao_nova_afericao.pack(pady=5, expand=True)

        # Botão "Histórico de Aferições"
        botao_historico = tk.Button(self, text="Histórico de Aferições", font=("Arial", 14), bg="white", fg="blue", 
                                    command=lambda: controller.show_frame(TelaHistorico))
        botao_historico.pack(pady=5, expand=True)

class TelaAfericao(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        global fonte_extra_bold
        self.configure(bg="#004AAD")
        
        fonte_extra_bold = Font(family="Arial", size=10, weight="bold")
        
        # Canvas e Scrollbar com expansão
        canvas = tk.Canvas(self, bg="#004AAD")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        main_frame = tk.Frame(canvas, bg="#004AAD")
        canvas.create_window((0, 0), window=main_frame, anchor="nw")

        # Expandir corretamente o conteúdo do frame principal
        main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # Informações do Posto Labels
        tk.Label(main_frame, text="Informações do Posto:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        tk.Label(main_frame, text="Empresa:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=1, column=1, sticky="w", padx=10)
        entry_empresa = criar_entry(main_frame, 70)
        entry_empresa.grid(row=1, column=2, sticky="w", padx=10)

        tk.Label(main_frame, text="CNPJ:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=1, column=3, sticky="w")
        entry_cnpj = criar_entry(main_frame, 20)
        entry_cnpj.grid(row=1, column=4, sticky="w", padx=10)

        tk.Label(main_frame, text="Endereço:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=2, column=1, sticky="w", padx=10)
        entry_endereco = criar_entry(main_frame, 70)
        entry_endereco.grid(row=2, column=2, sticky="w", padx=10)

        tk.Label(main_frame, text="Cidade:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=2, column=3, sticky="w")
        entry_cidade = criar_entry(main_frame, 20)
        entry_cidade.grid(row=2, column=4, sticky="w", padx=10)

        # Campos adicionais de identificação do dispenser
        tk.Label(main_frame, text="Nome do Dispenser:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=3, column=1, sticky="w", padx=10)
        entry_nome_dispenser = criar_entry(main_frame, 70)
        entry_nome_dispenser.grid(row=3, column=2, sticky="w", padx=10)

        tk.Label(main_frame, text="Número de Série:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=3, column=3, sticky="w")
        entry_numero_serie = criar_entry(main_frame, 20)
        entry_numero_serie.grid(row=3, column=4, sticky="w", padx=10)

        tk.Label(main_frame, text="Número do Lacre:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=4, column=1, sticky="w", padx=10)
        entry_numero_lacre = criar_entry(main_frame, 25)
        entry_numero_lacre.grid(row=4, column=2, sticky="w", padx=10)

        tk.Label(main_frame, text="Massa Específica:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=5, column=1, sticky="w", padx=10)
        massa_especifica_entry = criar_entry(main_frame, 25)
        massa_especifica_entry.grid(row=5, column=2, sticky="w", padx=10)

        tk.Label(main_frame, text="Lacre Após Aferição:", bg="#004AAD", fg="white", font=fonte_extra_bold).grid(row=6, column=1, sticky="w", padx=10)
        lacre_apos_entry = criar_entry(main_frame, 25)
        lacre_apos_entry.grid(row=6, column=2, sticky="w", padx=10)

        lado_a_entries = []
        lado_b_entries = []

        # Seções do lado esquerdo e direito
        criar_secao_lado("Lado A", 7, "A", main_frame, lado_a_entries, massa_especifica_entry)
        entry_numero_dispenser_a = tk.Entry(main_frame, bd=0, font=fonte_extra_bold, width=20)
        entry_numero_dispenser_a.grid(row=6, column=3, sticky="w", padx=10)
        entry_numero_dispenser_a.insert(0, f"Número Dispenser A")  # Placeholder para identificar o lado

        criar_secao_lado("Lado B", 17, "B", main_frame, lado_b_entries, massa_especifica_entry)
        entry_numero_dispenser_b = tk.Entry(main_frame, bd=0, font=fonte_extra_bold, width=20)
        entry_numero_dispenser_b.grid(row=16, column=3, sticky="w", padx=10)
        entry_numero_dispenser_b.insert(0, f"Número Dispenser B")  # Placeholder para identificar o lado


        # Botão para concluir e gerar o PDF
        btn_concluir = tk.Button(main_frame, text="Concluir Aferição", font=fonte_extra_bold, bg="green", fg="white", 
                                command=lambda: gerar_pdf(entry_empresa, entry_cnpj, entry_endereco, entry_cidade, entry_nome_dispenser,
                    entry_numero_serie, entry_numero_lacre, massa_especifica_entry, 
                    entry_numero_dispenser_a, entry_numero_dispenser_b, lado_a_entries, lado_b_entries))
        btn_concluir.grid(row=20, column=2, pady=10, columnspan=2)

        btn_voltar = tk.Button(main_frame, text="Voltar", font=fonte_extra_bold, bg="white", fg="blue", 
                                    command=lambda: controller.show_frame(TelaInicial))
        btn_voltar.grid(row=20, column=4, pady=10, columnspan=2)

class TelaHistorico(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(bg="#004AAD")

        # Fonte usada nas outras telas, aumentada para maior legibilidade
        fonte_extra_bold = Font(family="Arial", size=12, weight="bold")

        # Canvas para permitir rolagem
        canvas = tk.Canvas(self, bg="#004AAD")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame para os elementos dentro do canvas
        frame = tk.Frame(canvas, bg="#004AAD", width=900, height=800)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Expandir corretamente o conteúdo do frame dentro do canvas
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Criação do Treeview com formatação
        self.tree = ttk.Treeview(frame, columns=("Data", "Empresa", "CNPJ", "Endereço", "Cidade"), show="headings", height=15)
        self.tree.pack(fill="both", expand=True, padx=40, pady=40)

        # Definir as colunas da tabela
        colunas = ["Data", "Empresa", "CNPJ", "Endereço", "Cidade"]
        for coluna in colunas:
            self.tree.heading(coluna, text=coluna, anchor="center")
            self.tree.column(coluna, width=150, anchor="center")

        # Alterar o estilo da fonte dos dados
        style = ttk.Style()
        style.configure("Treeview", font=fonte_extra_bold)

        # Carregar os dados do histórico
        self.carregar_historico_ordenado()

        # Adicionar botão de download ao lado de cada item
        self.tree.bind("<Double-1>", self.baixar_pdf)

        # Criação de uma frame para os botões
        button_frame = tk.Frame(frame, bg="#004AAD")
        button_frame.pack(pady=20)

        # Botões na parte inferior
        self.btn_download = tk.Button(button_frame, text="Baixar PDF", command=self.baixar_pdf, bg="blue", fg="white", font=fonte_extra_bold)
        self.btn_download.pack(side="left", padx=10)

        self.btn_voltar = tk.Button(button_frame, text="Voltar", command=lambda: controller.show_frame(TelaInicial), bg="white", fg="blue", font=fonte_extra_bold)
        self.btn_voltar.pack(side="left", padx=10)

        # Botão de Atualizar
        self.btn_atualizar = tk.Button(button_frame, text="Atualizar", command=self.atualizar_dados, bg="green", fg="white", font=fonte_extra_bold)
        self.btn_atualizar.pack(side="left", padx=10)

    def carregar_historico_ordenado(self):
        """Consulta o banco e retorna o histórico ordenado por data/hora."""
        c.execute("SELECT id, data_hora, empresa, cnpj, endereco, cidade FROM afericoes ORDER BY data_hora DESC")
        historico = c.fetchall()

        # Limpar o Treeview antes de adicionar novos dados
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Adicionar os dados no Treeview
        for row in historico:
            self.tree.insert("", "end", values=row[1:6], tags=(row[0],))  # IDs como tags

    def atualizar_dados(self):
        """Função chamada pelo botão 'Atualizar' para recarregar os dados do banco."""
        self.carregar_historico_ordenado()

    def baixar_pdf(self, event=None):
        """Baixar PDF correspondente ao item selecionado."""
        # Caso o evento seja um duplo clique, pegamos o ID do item clicado
        if event:
            item_id = event.widget.item(event.widget.selection()[0], "tags")[0]
        else:
            item_id = self.tree.item(self.tree.selection())["tags"][0]
        
        # Buscar os dados do banco
        c.execute("SELECT * FROM afericoes WHERE id=?", (item_id,))
        dados = c.fetchone()
        
        if dados:
            # Organizar os dados para o PDF
            colunas = ["data_hora", "empresa", "cnpj", "endereco", "cidade", "nome_dispenser", "numero_serie", "numero_lacre", "massa_especifica"]
            dados_dict = dict(zip(colunas, dados[1:-2]))

            # Recuperar os dados do lado A e B
            lado_a_dados = dados[-2] if dados[-2] else ""
            lado_b_dados = dados[-1] if dados[-1] else ""
            
            # Solicitar local para salvar o PDF
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if file_path:
                # Gerar o PDF com os dados
                gerar_pdf_afericao(dados_dict, lado_a_dados, lado_b_dados, file_path)
                messagebox.showinfo("Sucesso", f"PDF salvo em {file_path}")
if __name__ == "__main__":
    app = App()
    app.mainloop()
