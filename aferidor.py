import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib import colors
from reportlab.platypus import  Table, TableStyle


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

def criar_secao_lado(titulo, inicio_y, lado, main_frame, entries_list):
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

        # Solicitar local para salvar o PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                                 filetypes=[("PDF files", "*.pdf")],
                                                 title="Salvar Arquivo PDF")
        if not file_path:
            return  # Cancelou a ação
        
        # Criar o PDF
        c = pdf_canvas.Canvas(file_path)
        largura, altura = 595.27, 841.89  # Dimensões padrão A4 em pontos (px)
        margem_esquerda = 50
        linha_atual = altura - 50

        # Configuração de fonte
        fonte_padrao = "Helvetica"
        c.setFont(fonte_padrao, 12)

        # Cabeçalho da empresa centralizado
        c.drawCentredString(largura / 2, linha_atual, "CF Serviços em Gás Natural")
        linha_atual -= 20
        c.drawCentredString(largura / 2, linha_atual, "CNPJ: 00.000.000/0001-00")
        linha_atual -= 15
        c.drawCentredString(largura / 2, linha_atual, "Endereço: Rua Fictícia, 123 - Cidade Exemplo")
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
        tabela_lado_a.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), fonte_padrao),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ]))
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
        tabela_lado_b.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), fonte_padrao),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ]))
        tabela_lado_b.wrapOn(c, largura, altura)
        tabela_lado_b.drawOn(c, margem_esquerda, linha_atual - 100)

        # Finalizar e salvar o PDF
        c.save()
        messagebox.showinfo("Sucesso", f"PDF salvo em {file_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")


# Configuração inicial da janela e fontes
root = tk.Tk()
root.title("Sistema de Aferição")
root.geometry("800x600")
fonte_extra_bold = Font(family="Arial", size=12, weight="bold")

# Canvas principal para rolagem
canvas = tk.Canvas(root, bg="#004AAD")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Usar grid para o layout do canvas e scrollbar
scrollbar.grid(row=0, column=1, sticky="ns")
canvas.grid(row=0, column=0, sticky="nsew")

# Configurações de expansão para o canvas no root
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Frame dentro do canvas para todo o conteúdo
main_frame = tk.Frame(canvas, bg="#004AAD")
canvas.create_window((0, 0), window=main_frame, anchor="nw")

# Atualiza a rolagem do canvas ao redimensionar o frame
main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

try:
    fonte_extra_bold = Font(family="Inter", size=10, weight="bold")
except:
    fonte_extra_bold = Font(size=10, weight="bold")  # Fallback se "Inter" não estiver disponível

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
criar_secao_lado("Lado A", 7, "A", main_frame, lado_a_entries)
entry_numero_dispenser_a = tk.Entry(main_frame, bd=0, font=fonte_extra_bold, width=20)
entry_numero_dispenser_a.grid(row=6, column=3, sticky="w", padx=10)
entry_numero_dispenser_a.insert(0, f"Número Dispenser A")  # Placeholder para identificar o lado

criar_secao_lado("Lado B", 17, "B", main_frame, lado_b_entries)
entry_numero_dispenser_b = tk.Entry(main_frame, bd=0, font=fonte_extra_bold, width=20)
entry_numero_dispenser_b.grid(row=16, column=3, sticky="w", padx=10)
entry_numero_dispenser_b.insert(0, f"Número Dispenser B")  # Placeholder para identificar o lado




# Botão para concluir e gerar o PDF
btn_concluir = tk.Button(main_frame, text="Concluir Aferição", font=fonte_extra_bold, bg="green", fg="white", 
                         command=lambda: gerar_pdf(entry_empresa, entry_cnpj, entry_endereco, entry_cidade, entry_nome_dispenser,
              entry_numero_serie, entry_numero_lacre, massa_especifica_entry, 
              entry_numero_dispenser_a, entry_numero_dispenser_b, lado_a_entries, lado_b_entries))
btn_concluir.grid(row=20, column=2, pady=10, columnspan=2)


root.mainloop()
