import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

# Função para calcular o Master Padrão (m³) e o erro para uma linha específica
def calcular_erro(entry_master_padrao_kg, entry_master_padrao_m3, entry_display_dispenser, entry_erro_percent, massa_especifica_entry):
    try:
        massa_especifica = float(massa_especifica_entry.get())
        master_padrao_kg = float(entry_master_padrao_kg.get())
        display_dispenser = float(entry_display_dispenser.get())
        
        # Calcula o valor de Master Padrão (m³) com base na massa específica
        master_padrao_m3 = master_padrao_kg / massa_especifica
        entry_master_padrao_m3.delete(0, tk.END)
        entry_master_padrao_m3.insert(0, f"{master_padrao_m3:.2f}")
        
        # Cálculo do erro (%)
        erro = ((display_dispenser - master_padrao_m3) / master_padrao_m3) * 100
        entry_erro_percent.delete(0, tk.END)
        entry_erro_percent.insert(0, f"{erro:.2f}")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Função para concluir aferição
def concluir_afericao():
    messagebox.showinfo("Aferição", "Aferição concluída com sucesso!")

def adicionar_nova_linha(parent_frame, entries_list, lado):
    # Criação dos campos de entrada para uma nova linha
    entry_master_padrao_kg = criar_entry(parent_frame, 15)
    entry_master_padrao_kg.grid(row=len(entries_list), column=0, padx=5, pady=5)
    
    entry_master_padrao_m3 = criar_entry(parent_frame, 15)
    entry_master_padrao_m3.grid(row=len(entries_list), column=1, padx=5, pady=5)
    
    entry_display_dispenser = criar_entry(parent_frame, 15)
    entry_display_dispenser.grid(row=len(entries_list), column=2, padx=5, pady=5)
    
    entry_erro_percent = criar_entry(parent_frame, 15)
    entry_erro_percent.grid(row=len(entries_list), column=3, padx=5, pady=5)
    
    # Botão para calcular o erro para essa linha específica
    btn_calcular = tk.Button(parent_frame, text="Calcular", 
                             command=lambda empkg=entry_master_padrao_kg, empm3=entry_master_padrao_m3, edd=entry_display_dispenser, eep=entry_erro_percent: calcular_erro(empkg, empm3, edd, eep, massa_especifica_entry),
                             font=fonte_extra_bold, bg="#004AAD", fg="white")
    btn_calcular.grid(row=len(entries_list), column=4, padx=5, pady=5)
    
    # Adiciona a nova linha à lista de entradas do lado correspondente
    entries_list.append((entry_master_padrao_kg, entry_master_padrao_m3, entry_display_dispenser, entry_erro_percent, btn_calcular))

# Função para criar uma seção de entrada com scroll
def criar_secao_lado(titulo, inicio_y, lado):
    # Título da seção
    tk.Label(root, text=titulo, bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=100, y=inicio_y)
    
    # Canvas com Scrollbar para a seção
    canvas = tk.Canvas(root, bg="#004AAD", width=800, height=300)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    
    # Frame interno onde os widgets de entrada serão colocados
    frame_lado = tk.Frame(canvas, bg="#004AAD")
    frame_lado.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Ligação do frame com o canvas
    canvas.create_window((0, 0), window=frame_lado, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Posicionamento do Canvas e da Scrollbar
    canvas.place(x=100, y=inicio_y + 30)
    scrollbar.place(x=900, y=inicio_y + 30, height=300)
    
    # Lista de entradas
    entries_list = []
    
    # Adiciona as primeiras 5 linhas de entrada
    for _ in range(5):
        adicionar_nova_linha(frame_lado, entries_list, lado)
    
    # Botão para adicionar novas linhas
    btn_adicionar = tk.Button(root, text="Adicionar Linha", command=lambda: adicionar_nova_linha(frame_lado, entries_list, lado),
                              bg="blue", fg="white", font=fonte_extra_bold)
    btn_adicionar.place(x=850, y=inicio_y)

def criar_entry(parent, largura):
    entry = tk.Entry(parent, bd=0, font=fonte_extra_bold, width=largura)
    return entry

# Criação da janela principal
root = tk.Tk()
root.title("AutoAferidor")
root.geometry("1000x1400")
root.configure(bg="#004AAD")

# Fonte personalizada
try:
    fonte_extra_bold = Font(family="Inter", size=10, weight="bold")
except:
    fonte_extra_bold = Font(size=10, weight="bold")  # Fallback se "Inter" não estiver disponível

# Labels e Entradas de Informações do Posto
tk.Label(root, text="Informações do Posto:", bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=20, y=10)
tk.Label(root, text="Empresa:", bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=20, y=50)
entry_empresa = criar_entry(root, 25)
entry_empresa.place(x=130, y=50)

tk.Label(root, text="CNPJ:", bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=360, y=50)
entry_cnpj = criar_entry(root, 20)
entry_cnpj.place(x=420, y=50)

# Endereço, Cidade e CEP
tk.Label(root, text="Endereço:", bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=20, y=100)
entry_endereco = criar_entry(root, 25)
entry_endereco.place(x=130, y=100)

tk.Label(root, text="Cidade:", bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=360, y=100)
entry_cidade = criar_entry(root, 20)
entry_cidade.place(x=420, y=100)

tk.Label(root, text="CEP:", bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=20, y=150)
entry_cep = criar_entry(root, 20)
entry_cep.place(x=130, y=150)

# Informações do Dispenser
tk.Label(root, text="Informações do Dispenser:", bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=20, y=200)
tk.Label(root, text="Número de Série Dispenser:", bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=20, y=240)
entry_num_serie_dispenser = criar_entry(root, 25)
entry_num_serie_dispenser.place(x=200, y=240)

tk.Label(root, text="Número do Lacre Encontrado:", bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=420, y=240)
entry_num_lacre_encontrado = criar_entry(root, 20)
entry_num_lacre_encontrado.place(x=600, y=240)

# Massa Específica
tk.Label(root, text="Massa Específica do Gás (kg/m³):", bg="#004AAD", fg="white", font=fonte_extra_bold).place(x=20, y=290)
massa_especifica_entry = tk.Entry(root, font=fonte_extra_bold)
massa_especifica_entry.place(x=250, y=290, width=150, height=30)

# Criar seções para Lado A e Lado B
criar_secao_lado("Lado A", 330, "A")
criar_secao_lado("Lado B", 700, "B")  # Disposto abaixo do Lado A

# Botões de conclusão e voltar
btn_concluir = tk.Button(root, text="Concluir Aferição", command=concluir_afericao, bg="green", fg="white", font=fonte_extra_bold)
btn_concluir.place(x=150, y=1200)

btn_voltar = tk.Button(root, text="Voltar", command=root.quit, bg="red", fg="white", font=fonte_extra_bold)
btn_voltar.place(x=300, y=1200)

root.mainloop()
