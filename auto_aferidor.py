import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk  # Add PIL to handle the image

def concluir_afericao():
    messagebox.showinfo("Aferição", "Aferição concluída com sucesso!")

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
    entry_numero_dispenser = criar_entry(parent_frame, 10)
    entry_numero_dispenser.grid(row=len(entries_list) + 1, column=0, padx=5, pady=5)
    
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
    
    entries_list.append((entry_numero_dispenser, entry_master_padrao_kg, entry_master_padrao_m3, entry_display_dispenser, entry_erro_percent, btn_calcular))

def criar_secao_lado(titulo, inicio_y, lado, main_frame):
    # Título da seção e campo de entrada para "Número Dispenser"
    label_titulo = tk.Label(main_frame, text=titulo, bg="#004AAD", fg="white", font=fonte_extra_bold)
    label_titulo.grid(row=inicio_y, column=2, sticky="w", padx=10)
    
    entry_numero_dispenser = tk.Entry(main_frame, bd=0, font=fonte_extra_bold, width=10)
    entry_numero_dispenser.grid(row=inicio_y, column=3, sticky="w", padx=10)
    entry_numero_dispenser.insert(0, f"Número {lado}")  # Placeholder para identificar o lado

    # Frame para as entradas da seção
    frame_lado = tk.Frame(main_frame, bg="#004AAD")
    frame_lado.grid(row=inicio_y + 1, column=2, sticky="w", padx=10, pady=10)
    
    # Labels das colunas
    labels = ["Master kg", "Master m³", "Dispenser m³", "Erro %"]
    for i, text in enumerate(labels):
        label = tk.Label(frame_lado, text=text, bg="#004AAD", fg="white", font=fonte_extra_bold)
        label.grid(row=0, column=i, padx=5, pady=5)

    # Lista para armazenar entradas e campo de média de erro
    entries_list = []
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

root = tk.Tk()
root.title("AutoAferidor")
root.geometry("1440x900")
root.configure(bg="#004AAD")

# Load and display the image
image_path = "/Users/pedri/OneDrive/Área de Trabalho/pedro/AferidorTcc/Inserir um título 2.png"
image = Image.open(image_path)
image = image.resize((100, 100), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo, bg="#004AAD")
image_label.image = photo 
image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

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

# Seções do lado esquerdo e direito
criar_secao_lado("Lado A", 6, "A", main_frame)
criar_secao_lado("Lado B", 16, "B", main_frame)

btn_concluir = tk.Button(main_frame, text="Concluir Aferição", command=concluir_afericao, font=fonte_extra_bold, bg="green", fg="white")
btn_concluir.grid(row=20, column=3, padx=10, pady=10, sticky="w")

root.mainloop()
