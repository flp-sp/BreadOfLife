import customtkinter as ctk
from parser_usfx import parse_usfx
from tkinter import filedialog

# Parse da Bíblia
biblia = parse_usfx('por-almeida.usfx.xml')

global testamentoAtual

# Configurações iniciais
ctk.set_appearance_mode('dark')

janela = ctk.CTk()
janela.title('Bread of Life')
janela.geometry('1080x600')

# Configuração da grid
janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(1, weight=1)

frame_menu = ctk.CTkFrame(janela, width=200)
frame_menu.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

notas = ctk.CTkFrame(janela, width=250)
notas.grid(row=0, column=2, sticky="ns", padx=10, pady=10)

strong = ctk.CTkFrame(janela)
strong.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

# Menu de livros
labelAntigo = ctk.CTkLabel(frame_menu,font=('Arial', 18), text="Antigo Testamento")
labelAntigo.grid(row=0, column=0, sticky="ew", pady=3)

antigo = ctk.CTkOptionMenu(frame_menu, font=('Arial', 16),
                            values=['GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA', '2SA', '1KI', '2KI', '1CH', '2CH', 'EZR', 'NEH', 'EST', 'JOB', 'PSA', 'PRO', 'ECC', 'SNG', 'ISA', 'JER', 'LAM', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO', 'OBA', 'JON', 'MIC', 'NAM', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL'])
antigo.grid(row=1, column=0, sticky="ew", pady=3, padx=10)

labelNovo = ctk.CTkLabel(frame_menu,font=('Arial', 18), width=280, text="Novo Testamento")
labelNovo.grid(row=2, column=0, sticky="ew", pady=3)

novo = ctk.CTkOptionMenu(frame_menu, font=('Arial', 16),
                          values=['MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV'])
novo.grid(row=3, column=0, sticky="ew", pady=3, padx=10)

# botao selecionar capitulo
capitulo_btn = ctk.CTkButton(frame_menu,font=('Arial', 16), text="Selecionar Capítulo")
capitulo_btn.grid(row=4, column=0, sticky="ew", pady=5, padx=10)

testamentoAtual = ''

# selecionar capitulo func
def abrir_lista_capitulos():
    global testamentoAtual
    janela_cap = ctk.CTkToplevel(janela)
    janela_cap.title("Escolha o Capítulo")
    janela_cap.geometry("200x300")

    scroll = ctk.CTkScrollableFrame(janela_cap)
    scroll.pack(fill="both", expand=True, padx=5, pady=5)

    book = ''
    if testamentoAtual == 'antigo':
        book = antigo.get()
    elif testamentoAtual == 'novo':
        book = novo.get()

    if book in biblia:
        for cap in biblia[book]:
            ctk.CTkButton(scroll, text=str(cap),
                          command=lambda cap=cap: selecionar_capitulo(cap, janela_cap)).pack(pady=2)

def selecionar_capitulo(cap, janela_cap):
    capitulo_btn.configure(text=f"Capítulo {cap}")
    janela_cap.destroy()

# testamento atual
def triggerAntigo(x):
    global testamentoAtual
    testamentoAtual = 'antigo'
def triggerNovo(x):
    global testamentoAtual
    testamentoAtual = 'novo'

#botao de pesquisa
botao = ctk.CTkButton(frame_menu, font=('Arial', 16), text='Pesquisar')
botao.grid(row=5, column=0, sticky="ew", padx=5,pady=5)

# biblia texto
texto = ctk.CTkTextbox(janela, wrap="word", font=('Arial', 18), state='disabled')
texto.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# mostrar o texto e pegar o livro
def select_book():
    texto.configure(state='normal')
    texto.delete("1.0", "end")
    book = ''
    if testamentoAtual == 'antigo':
        book = antigo.get()
    elif testamentoAtual == 'novo':
        book = novo.get()
    currentCap = capitulo_btn.cget("text").replace("Capítulo ", "")
    temp = ''
    if book in biblia and currentCap in biblia[book]:
        for num, verso in biblia[book][currentCap]:
            temp += f'{num} {verso}\n'
    else:
        temp = 'Capítulo não encontrado.'
        print(f'{book} {testamentoAtual}')
    texto.insert("1.0", temp)
    texto.configure(state='disabled')

def _salvar():
    arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de texto", "*.txt")])

    if arquivo:
        conteudo = textNota.get("1.0", "end-1c")
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)

def _abrir():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt")])
    if arquivo:
        # Lê o conteúdo do arquivo
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
        # Limpa o textbox e insere o conteúdo
        textNota.delete("1.0", "end")
        textNota.insert("1.0", conteudo)
        print(f"Arquivo aberto: {arquivo}")

# bloco de notas
textNota = ctk.CTkTextbox(notas,width=350, wrap="word")
textNota.pack(expand=True, fill="both", padx=10, pady=10)

salvar = ctk.CTkButton(notas, text="Salvar como .txt", command=_salvar)
salvar.pack(pady=10)

abrir = ctk.CTkButton(notas, text="Abrir nota", command=_abrir)
abrir.pack(pady=10)

botao.configure(command=select_book)
antigo.configure(command=triggerAntigo)
novo.configure(command=triggerNovo)
capitulo_btn.configure(command=abrir_lista_capitulos)

janela.mainloop()