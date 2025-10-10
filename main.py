import customtkinter as ctk
from parser_almeida import parse_usfx
from tkinter import filedialog

from parser_kjv import parse_kjv
from parser_grego import parse_grego

biblia = parse_usfx('por-almeida.usfx.xml')
currentCap = ''

global testamentoAtual

# janela config
ctk.set_appearance_mode('dark')

janela = ctk.CTk()
janela.title('Bread of Life')
janela.geometry('1080x600')

# configuracao da janela principal
janela.grid_rowconfigure(1, weight=1)
janela.grid_columnconfigure(1, weight=1)

# menu lateral
frame_menu = ctk.CTkFrame(janela, width=200)
frame_menu.grid(row=0, column=0, rowspan=2, sticky="ns", padx=10, pady=10)

# bloco de notas
notas = ctk.CTkFrame(janela, width=250)
notas.grid(row=0, column=2, rowspan=2, sticky="ns", padx=10, pady=10)

# capitulos
capitulos = ctk.CTkFrame(frame_menu)
capitulos.grid(row=6,column=0)

# strong
strong = ctk.CTkFrame(janela)
strong.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

# mudar biblias ou paginas (segmento acima do texto)
segment = ctk.CTkFrame(janela)
segment.grid(row=0, column=1, sticky="ew", padx=10, pady=(10, 0))

selecionarBiblia = ctk.CTkSegmentedButton(segment, values=['Almeida', 'KJV', 'Grego NT'])
selecionarBiblia.set('Almeida')
selecionarBiblia.pack(fill="x", padx=10, pady=10)

# biblia texto
texto = ctk.CTkTextbox(janela, wrap="word", font=('Arial', 18), state='disabled')
texto.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0, 10))

# menu de livros
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

# label selecionar capitulo
capituloLabel = ctk.CTkLabel(frame_menu,font=('Arial', 16), text="Selecione um livro")
capituloLabel.grid(row=4, column=0, sticky="ew", pady=5, padx=10)

testamentoAtual = ''

# funcao para selecionar versao e trocar o texto
def selecionarVersao(versao):
    global biblia
    match versao:
        case 'Almeida':
            biblia = parse_usfx('por-almeida.usfx.xml')
            if currentCap != '':
                select_book()
        case 'KJV':
            biblia = parse_kjv('eng-kjv2006_usfx.xml')
            if currentCap != '':
                select_book()
        case 'Grego NT':
            biblia = parse_grego('grcbyz_usfx.xml')
            if currentCap != '':
                select_book()

selecionarBiblia.configure(command=selecionarVersao)

# selecionar capitulo func
def abrir_lista_capitulos():
    global testamentoAtual
    global scroll

    scroll = ctk.CTkScrollableFrame(capitulos)
    scroll.pack(fill="both", expand=True, padx=5, pady=5)

    book = ''
    if testamentoAtual == 'antigo':
        book = antigo.get()
    elif testamentoAtual == 'novo':
        book = novo.get()

    if book in biblia:
        for cap in biblia[book]:
           ctk.CTkButton(scroll, text=str(cap),command=lambda cap=cap: selecionar_capitulo(cap, capitulos)).pack(pady=2)

def selecionar_capitulo(cap, janela_cap):
    global currentCap
    currentCap = cap
    capituloLabel.configure(text=f"Capitulo {cap}")
    select_book()

# testamento atual
def triggerAntigo(x):
    global testamentoAtual
    global scroll
    if testamentoAtual == 'antigo' or testamentoAtual == 'novo':
        scroll.pack_forget()
    testamentoAtual = 'antigo'
    capituloLabel.configure(text="Selecionar Capitulo")
    abrir_lista_capitulos()

def triggerNovo(x):
    global testamentoAtual
    global scroll
    if testamentoAtual == 'antigo' or testamentoAtual == 'novo':
        scroll.pack_forget()
    testamentoAtual = 'novo'
    capituloLabel.configure(text="Selecionar Capitulo")
    abrir_lista_capitulos()

# mostrar o texto e pegar o livro
def select_book():
    global currentCap
    texto.configure(state='normal')
    texto.delete("1.0", "end")
    book = ''
    if testamentoAtual == 'antigo':
        book = antigo.get()
    elif testamentoAtual == 'novo':
        book = novo.get()
    temp = ''
    if book in biblia and currentCap in biblia[book]:
        for num, verso in biblia[book][currentCap]:
            temp += f'{num} {verso}\n'
    else:
        temp = 'Capítulo não encontrado.'
        print(f'{book} {testamentoAtual}')
    texto.insert("1.0", temp)
    texto.configure(state='disabled')

# salvar nota
def _salvar():
    arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de texto", "*.txt")])
    if arquivo:
        conteudo = textNota.get("1.0", "end-1c")
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)

# abrir nota
def _abrir():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt")])
    if arquivo:
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
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

# configurar botoes dos menus
antigo.configure(command=triggerAntigo)
novo.configure(command=triggerNovo)

# loop principal
janela.mainloop()