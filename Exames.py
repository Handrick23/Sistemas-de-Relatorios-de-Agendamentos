# PROGRAMA DE GERAÇÃO DE RELATÓRIOS DE EXAMES MÉDICOS
#
# DESENVOLVEDOR: HANDRICK GUIMARÃES

# IMPORTANDO BIBLIOTECAS:

from logging import root
import customtkinter as ctk
import pandas as pd
import tkinter as tk
import sys
import os
from PIL import Image as PILImage
import threading
import base64
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import LongTable
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.units import cm
from tkinter import ttk
from io import BytesIO
from tkinter import filedialog

# CRIANDO A BASE DE DADOS:
lista_colunas = ["PACIENTE", "TELEFONE", "PROCEDIMENTO", "INSTITUIÇÃO", "AGEND./CAPITAÇÃO", "ENVIO"]
exames_relatorio = pd.DataFrame(columns=lista_colunas)

#HOSPITAIS E CONSULTAS ACEITOS:
hospitais = [
    "Hospital Santa Isabel",
    "Hospital da Mulher",
    "Hospital Couto Maia",
    "Hospital Agenor Paiva",
    "Hospital Professor Edgar Santos",
    "CIMEB",
    "Clínica AFAC",
    "Clínica Histocito Biopsias",
    "HISTOCITO",
    "Hospital Sarah",
    "Hospital Manoel Vitorino",
    "Hospital Irmã Dulce Ribeira",
    "Ambulatório Magalhães Neto",
    "Hospital Ana Nery",
    "Hospital da Bahia",
    "Hospital Otávio Mangabeira",
    "Hospital Aristides Maltês",
    "Hospital Geral Ernesto Simões",
    "HGE",
    "Hospital Geral Roberto Santos",
    "Hospital Santa Luzia",
    "Hospital Português",
    "Hospital Juliano Moreira",
    "CEDAP 02",
    "Hospital Irmã Dulce Patamares",
    "Hospital do Homem Monte Serrá",
    "Faculdade ZARN",
    "Faculdade FTC",
    "ADAB Baiana",
    "CEDAF UFBA",
    "CEPRED",
    "ICS UFBA",
    "CEDEBA",
    "APAE",
    "HEMOBA",
    "IBOPC",
    "Hospital do Suburbio",
    "Hospital Municipal",
    "Hospital Metropolitano",
    "Faculdade Unijorge",
    "Faculdade Uni Dom Pedro",
    "Multi Centro Carlos Gomes",
    "Faculdade de Odontologia da UFBA",
    "CICAM",
    "Martagão Gesteira",
    "IOBA",
    "CDTO",
    "DULCIMED",
    "Instituto dos Cegos da Bahia",
    "Maternidade Climério de Oliveira",
    "HOEB",
    "Hospital Eládio",
    "Hospital Alayde Costa",
    "Hospital 2 de Julho", 
    "Hospital Professor Carvalho Luz",
    "Hospital Mário Leal",
    "Maternidade Professor José Maria de Magalhães Neto",
    "CEDAR"
]
consultas = [
    "Otorrinolaringologista",
    "Reumatologista",
    "Cardiologista",
    "Hematologista",
    "Cabeça E Pescoço",
    "Cirurgião Torácico",
    "Gastro",
    "Hepatologista",
    "Endocrinologista",
    "Bucomaxilo",
    "Triagem Oncológica",
    "Urologista",
    "Ginecologista",
    "Mastologista",
    "Neurologista",
    "Neurocirurgião",
    "Clínica Da Dor",
    "Ambulatório Do Sono",
    "Cirurgião Pediátrico",
    "Alergologista",
    "Oftalmologista",
    "Neuro Oftalmo",
    "Ortopedista",
    "Clínica Da Obesidade",
    "Cirurgião Vascular",
    "Cirurgião Geral",
    "Estomatologista",
    "Anestesista",
    "Nutricionista",
    "Enfermagem",
    "Serviço Social",
    "PAPO",
    "Angiologista",
    "Nefrologista",
    "Coloproctologista",
    "Dermatologista",
    "Psiquiatra",
    "Psicólogo",
    "Fonoaudiólogo",
    "Fisioterapeuta",
    "Terapeuta Ocupacional",
    "Nutrólogo",
    "Infectologista",
    "Pediatra",
    "Clínico Geral",
    "Geriatra",
    "Pneumologista",
    "Cirurgião Plástico",
    "Obstetra",
    "Geneticista",
    "Ambulatório Trans",
    "Odontologista",
    "Dentista", 
    "Hipertensão Pulmonar",
    "Cirurgia Bariátrica",
    "Ambulatório Do Adolescente",
    "Onco Emato",
    "Imunologista",
]
  
# TODAS AS FUNÇÕES USADAS NO PROGRAMA:
def salvar():

    # Acessando as variáveis globais:
    global exames_relatorio, hospitais, consultas

    lista_objetos = []
    dias = [
    "01","02","03","04","05","06","07","08","09", "10"
    ,"11","12","13","14","15","16","17","18","19", "20"
    ,"21","22","23","24","25","26","27","28","29", "30", "31"
    ]
    meses = [
        "01","02","03","04","05","06","07","08","09", "10", "11", "12"
        ]
    anos = [
        "2022", "2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030", "2031", "2032", "2033", "2034", "2035"
        ]
    horarios = [
        f"{h:02d}:{m:02d}" for h in range(24) for m in range(60)
    ]

    # --- TRATAMENTO DOS DADOS ---

    # OBTENDO AS INFORMAÇÕES:
    save_nome = nome_.get().strip().title()
    save_tel = tel_.get().strip()
    save_proc = procedimentos_possiveis.get().strip()
    save_deta = deta_.get().strip().title()
    save_inst = inst_.get().strip()
    save_data = data_.get().strip()
    save_horario = horario_.get().strip()
    save_env = env_.get().strip()
    save_adulto = adulto_.get().strip()

    # -> VALIDAÇÕES:

    # CAMPOS VAZIOS
    if not save_nome:
        tela_erro = ctk.CTk()
        tela_erro.title("ERRO - PACIENTE VAZIO")
        tela_erro.geometry("600x190")
        erro = ctk.CTkLabel(
            tela_erro,
            text="\n NOME INVÁLIDO \n\n Paciente sem nome digitado!",
            font=("Arial", 23)
        )
        erro.pack()
        tela_erro.mainloop()
        return
    
    if not save_tel:
        tela_erro1 = ctk.CTk()
        tela_erro1.title("ERRO - TELEFONE VAZIO")
        tela_erro1.geometry("600x190")
        erro1 = ctk.CTkLabel(
            tela_erro1,
            text="\n TELEFONE INVÁLIDO \n\n Paciente sem número digitado!",
            font=("Arial", 23)
        )
        erro1.pack()
        tela_erro1.mainloop()
        return
    if not save_proc:
        tela_erro2 = ctk.CTk()
        tela_erro2.title("ERRO - PROCEDIMENTO VAZIO")
        tela_erro2.geometry("600x190")
        erro2 = ctk.CTkLabel(
            tela_erro2,
            text="\n PROCEDIMENTO INVÁLIDO \n\n Escolha e selecione pelo menos uma opção!",
            font=("Arial", 23)
        )
        erro2.pack()
        tela_erro2.mainloop()
        return
    if not save_deta:
        tela_erro3 = ctk.CTk()
        tela_erro3.title("ERRO - DETALHAMENTO VAZIO")
        tela_erro3.geometry("600x190")
        erro3 = ctk.CTkLabel(
            tela_erro3,
            text="\n DETALHAMENTO INVÁLIDO \n\n Especifique as observações do procedimento!",
            font=("Arial", 23)
        )
        erro3.pack()
        tela_erro3.mainloop()
        return
    if not save_data:
        tela_erro4 = ctk.CTk()
        tela_erro4.title("ERRO - DATA VAZIA")
        tela_erro4.geometry("600x190")
        erro4 = ctk.CTkLabel(
            tela_erro4,
            text="\n DATA INVÁLIDA \n\n Digite a data do agendamento!",
            font=("Arial", 23)
        )
        erro4.pack()
        tela_erro4.mainloop()
        return
    if not save_horario:
        tela_erro5 = ctk.CTk()
        tela_erro5.title("ERRO - HORARIO VAZIO")
        tela_erro5.geometry("600x190")
        erro5 = ctk.CTkLabel(
            tela_erro5,
            text="\n HORÁRIO INVÁLIDO \n\n Digite o horário do agendamento!!",
            font=("Arial", 23)
        )
        erro5.pack()
        tela_erro5.mainloop()
        return
    
    if not save_env:
        tela_erro6 = ctk.CTk()
        tela_erro6.title("ERRO - ENVIO VAZIO")
        tela_erro6.geometry("600x190")
        erro6 = ctk.CTkLabel(
            tela_erro6,
            text="\n ENVIO INVÁLIDO \n\n Digite os detalhes do envio!",
            font=("Arial", 23)
        )
        erro6.pack()
        tela_erro6.mainloop()
        return
        
    
    # VALIDANDO OS HOSPITAIS:

    if save_inst not in hospitais:
        tela_erro = ctk.CTk()
        tela_erro.title("HOSPITAL INVÁLIDO")
        tela_erro.geometry('640x260')
        erro = ctk.CTkLabel(tela_erro, text="HOSPITAL INVÁLIDO! \n\n Consulte a lista de hospitais aceitos, ou reveja a escrita! \n\n\n\n Exemplo: Hospital Santa Isabel, Hospital Ana Nery, HGE...", font=("Arial", 23))
        erro.pack()
        tela_erro.mainloop()
        return
    
    # VALIDANDO O TELEFONE:

    if len(save_tel) < 8 or len(save_tel) > 11 or not save_tel.isdigit():
        if not isinstance(save_tel, int):
            try:
                int(save_tel)
            except ValueError:
                tela_erro = ctk.CTk()
                tela_erro.title("TELEFONE INVÁLIDO")
                tela_erro.geometry('600x190')
                erro = ctk.CTkLabel(tela_erro, text="Número de telefone inválido! \n\n Há letras/simbolos no valor digitado.", font=("Arial", 23))
                erro.pack()
                tela_erro.mainloop()
                return
        tela_erro = ctk.CTk()
        tela_erro.title("TELEFONE INVÁLIDO")
        tela_erro.geometry('600x190')
        erro = ctk.CTkLabel(tela_erro, text="Número de telefone inválido! \n\n Verifique se o número está correto.", font=("Arial", 23))
        erro.pack()
        tela_erro.mainloop()
        return
    

    # VALIDANDO A DATA:

    # -> TAMANHO DA STRING E AS BARRAS:
    if len(save_data) != 10 or save_data[2] != '/' or save_data[5] != '/':
        tela_erro = ctk.CTk()
        tela_erro.title("DATA INVÁLIDA")
        tela_erro.geometry('600x190')
        erro = ctk.CTkLabel(tela_erro, text="Data inválida! \n\n Verifique se a data está correta.\n\n\n Exemplo: 01/01/2001", font=("Arial", 23))
        erro.pack()
        tela_erro.mainloop()
        return
    # -> VALIDANDO SE SÃO NÚMEROS:
    if not (save_data[:2].isdigit() and save_data[3:5].isdigit() and save_data[6:].isdigit()):
        tela_erro = ctk.CTk()
        tela_erro.title("DATA INVÁLIDA")
        tela_erro.geometry('600x190')
        erro = ctk.CTkLabel(tela_erro, text="Data inválida! \n\n Verifique se a data está correta.\n\n\n Exemplo: 01/01/2001", font=("Arial", 23))
        erro.pack()
        tela_erro.mainloop()
        return
    # -> VALIDANDO SE OS NÚMEROS ESTÃO NA LISTA:
    if save_data[:2] not in dias or save_data[3:5] not in meses or save_data[6:] not in anos:
        tela_erro = ctk.CTk()
        tela_erro.title("DATA INVÁLIDA")
        tela_erro.geometry('600x190')
        erro = ctk.CTkLabel(tela_erro, text="Data inválida! \n\n Verifique se a data está correta.\n\n\n Exemplo: 01/01/2001", font=("Arial", 23))
        erro.pack()
        tela_erro.mainloop()
        return
    
    # VALIDANDO O HORÁRIO:
    if save_horario not in horarios:
        tela_erro = ctk.CTk()
        tela_erro.title("HORÁRIO INVÁLIDO")
        tela_erro.geometry('600x190')
        erro = ctk.CTkLabel(tela_erro, text="Horário inválido! \n\n Verifique se o horário está correto.\n\n\n Exemplo: 08:30, 14:45, 23:59...", font=("Arial", 20))
        erro.pack()
        tela_erro.mainloop()
        return
    
    # VALIDANDO AS CONSULTAS:
    
    if save_proc == "CONSULTA" and save_deta not in consultas:
        tela_erro = ctk.CTk()
        tela_erro.title("CONSULTA INVÁLIDA")
        tela_erro.geometry('680x250')
        erro = ctk.CTkLabel(tela_erro, text="Tipo de CONSULTA inválida! \n\n Consulte a lista de consultas aceitas, ou reveja a escrita. \n\n (Exemplo: Otorrinolaringologista, Reumatologista, Cardiologista...)", font=("Arial", 23))
        erro.pack()
        tela_erro.mainloop()
        return
    
    # ADICIONANCO QUANDO FOR PEDIÁTRICO:
    if save_adulto == "PEDIATRICO":
        save_deta = f'{save_deta} - PEDIÁTRICO'
    proc_final = str(f'{save_proc}: {save_deta}')

    # CONFIGURANDO O AGENDAMENTO:
    agendamento = f'{save_data},  às {save_horario}h'

    # ADICIONANDO OS DADOS NA BASE:
    global exames_relatorio
    exames_relatorio.loc[len(exames_relatorio)] = [save_nome, save_tel, proc_final, save_inst, agendamento, save_env]

    # DELETANDO OS ENTRYS:
    tel_.delete(0, tk.END)
    procedimentos_possiveis.set("")
    nome_.delete(0, tk.END)
    deta_.delete(0, tk.END)
    inst_.delete(0, tk.END)
    data_.delete(0, tk.END)
    env_.delete(0, tk.END)
    horario_.delete(0, tk.END)

    # FEEDBACK POSITIVO:
    tela_sucesso = ctk.CTk()
    tela_sucesso.title("PACIENTE SALVO")
    tela_sucesso.geometry('350x190')
    sucesso = ctk.CTkLabel(tela_sucesso, text="\n\nSALVO COM SUCESSO! \n\n\n (Paciente já na base de dados!)", font=("Arial", 23))
    sucesso.pack()

    tela_sucesso.mainloop()

def sugestao_hospital(event=None):
    typed = inst_.get().lower()

    if not typed:
        suggestion_frame.place_forget()
        return

    matches = [h for h in hospitais if typed in h.lower()]

    if matches:
        suggestion_frame.place(x=inst_.winfo_x(), y=inst_.winfo_y()+30)
        suggestion_frame.lift()

        current_labels = suggestion_frame.winfo_children()
        if len(current_labels) != len(matches):
            for widget in current_labels:
                widget.destroy()

            for hospital in matches:
                lbl = ctk.CTkLabel(
                    suggestion_frame,
                    text=hospital,
                    fg_color="white",
                    text_color="black",
                    corner_radius=5
                )
                lbl.pack(fill="x", padx=2, pady=1)
                lbl.bind("<Button-1>", lambda e, h=hospital: encontrar_hospital(h))
        else:
            for lbl, hospital in zip(current_labels, matches):
                lbl.configure(text=hospital)
    else:
        suggestion_frame.place_forget()

def encontrar_hospital(hospital):
    inst_.delete(0, "end")
    inst_.insert(0, hospital)
    suggestion_frame.place_forget()

def sugestao_consultas(event=None):
    if procedimentos_possiveis.get().strip().upper() != "CONSULTA":
        consulta_frame.place_forget()
        return

    typed = deta_.get().lower()

    if not typed:
        consulta_frame.place_forget()
        return

    matches = [c for c in consultas if typed in c.lower()]

    if matches:
        consulta_frame.place(x=deta_.winfo_x(), y=deta_.winfo_y()+30)
        consulta_frame.lift()

        current_labels = consulta_frame.winfo_children()
        if len(current_labels) != len(matches):
            for widget in current_labels:
                widget.destroy()

            for consulta in matches:
                lbl = ctk.CTkLabel(
                    consulta_frame,
                    text=consulta,
                    fg_color="white",
                    text_color="black",
                    corner_radius=5
                )
                lbl.pack(fill="x", padx=2, pady=1)
                lbl.bind("<Button-1>", lambda e, c=consulta: encontrar_consulta(c))
        else:
            for lbl, consulta in zip(current_labels, matches):
                lbl.configure(text=consulta)
    else:
        consulta_frame.place_forget()

def encontrar_consulta(consulta):
    deta_.delete(0, "end")
    deta_.insert(0, consulta)
    consulta_frame.place_forget()

def limpar():
    # DELETANDO OS VALORES NOS ENTRYS:
    tel_.delete(0, tk.END)
    procedimentos_possiveis.set("")
    nome_.delete(0, tk.END)
    deta_.delete(0, tk.END)
    inst_.delete(0, tk.END)
    data_.delete(0, tk.END)
    env_.delete(0, tk.END)

def excluir():
    # CRIANDO A JANELA:
    tela_excluir = ctk.CTk()
    tela_excluir.title("EXCLUIR")
    tela_excluir.geometry('550x230')
    lbl = ctk.CTkLabel(tela_excluir, text=" Excluir paciente? \n\n Digite o nome completo do paciente:")
    lbl.pack(pady=10)

    # BOTÃO DE EXCLUSÃO:
    entry_nome = ctk.CTkEntry(tela_excluir, width=400, height=25)
    entry_nome.pack(pady=10)

    # FUNÇÃO PARA CONFIRMAR EXCLUSÃO:
    def confirmar_exclusao():
        global exames_relatorio
        nome_para_excluir = entry_nome.get().strip().title()
        if not nome_para_excluir:
            return
        
        # SE TIVER MAIS DE UM COM O MESMO NOME, EXCLUIRÁ O ÚLTIMO ADICIONADO:
        if nome_para_excluir in exames_relatorio['PACIENTE'].values:
            indice_ultimo = exames_relatorio[exames_relatorio['PACIENTE'] == nome_para_excluir].index[-1]
            exames_relatorio = exames_relatorio.drop(indice_ultimo)
            tela_sucesso = ctk.CTk()
            tela_sucesso.title("SUCESSO!")
            tela_sucesso.geometry('400x150')
            sucesso = ctk.CTkLabel(tela_sucesso, text="\n Paciente excluído com sucesso!", font=("Arial", 18))
            sucesso.pack()
            tela_excluir.destroy()
            tela_sucesso.mainloop()
        # SE NÃO HOUVER PACIENTES ADICIONADOS, NÃO EXCLUI NINGUÉM:
        if exames_relatorio.empty:
            tela_erro = ctk.CTk()
            tela_erro.title("ERRO")
            tela_erro.geometry('400x150')
            erro = ctk.CTkLabel(tela_erro, text="\n Base de dados vazia! \n\n Adicione pacientes antes de excluir.", font=("Arial", 18))
            erro.pack()
            tela_erro.mainloop()
            return

        # SE NÃO ENCONTRAR NOME, RETORNA UMA JANELA FALANDO ISSO:
        if nome_para_excluir not in exames_relatorio['NOME DO PACIENTE'].values:
            tela_erro = ctk.CTk()
            tela_erro.title("ERRO")
            tela_erro.geometry('400x150')
            erro = ctk.CTkLabel(tela_erro, text="\n Paciente não encontrado! \n\n Verifique o nome digitado.", font=("Arial", 18))
            erro.pack()
            tela_erro.mainloop()
            return
        
    # BOTÃO DE CONFIRMAÇÃO DA EXCLUSÃO:        
    botao_confirmar = ctk.CTkButton(tela_excluir, text="EXCLUIR", command=confirmar_exclusao, fg_color="#800C0C")
    botao_confirmar.pack(pady=10)

    tela_excluir.mainloop()

def visualizar():
    global exames_relatorio
    global lista_colunas
    colunas = lista_colunas

    # CONFIGURANDO A APARENCIA GERAL:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("1200x600")
    root.title("Exames - Base de Dados")

    # ESTILO:
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#2b2b2b",
                    foreground="white",
                    rowheight=25,
                    fieldbackground="#2b2b2b")
    style.map("Treeview",
            background=[("selected", "#1f6aa5")])
    
    # CONFIGURANDO ABA DE VISUALIZAÇÃO:
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    scroll_y = ctk.CTkScrollbar(frame, orientation="vertical")
    scroll_y.pack(side="right", fill="y")

    scroll_x = ctk.CTkScrollbar(frame, orientation="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    tree = ttk.Treeview(frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    tree.pack(fill="both", expand=True)

    scroll_y.configure(command=tree.yview)
    scroll_x.configure(command=tree.xview)

    # COLUNAS: 
    tree["columns"] = colunas
    tree["show"] = "headings" 

    for i, row in exames_relatorio.iterrows():
        tree.insert("", "end", values=list(row))

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    root.mainloop()
    return

def relatorio():
    global assinatura_, ano_, mes_, contato_, tela_relatorio, cidade_

    # JANELA DE RELATÓRIO:
    tela_relatorio = ctk.CTk()
    tela_relatorio.title("RELATÓRIO")
    tela_relatorio.geometry('600x700')
    
    # MUNICÍPIO:

    cidade = ctk.CTkLabel(tela_relatorio, text="MUNICÍPIO:", font=("Arial", 13))
    cidade.pack(pady=10)
    cidade_ = ctk.CTkEntry(tela_relatorio, width=400, height=25)
    cidade_.pack(pady=10)

    # ASSINATURA DO RELATOR:
    assinatura = ctk.CTkLabel(tela_relatorio, text="NOME DO MARCADOR(A):")
    assinatura.pack(pady=10)
    assinatura_ = ctk.CTkEntry(tela_relatorio, width=500, height=25)
    assinatura_.pack(pady=10)

    # ANO DO RELATÓRIO:
    ano = ctk.CTkLabel(tela_relatorio, text="ANO DO RELATÓRIO:")
    ano.pack(pady=10)
    ano_ = ctk.CTkEntry(tela_relatorio, width=100, height=25)
    ano_.pack(pady=10)

    # MÊS DO RELATÓRIO:
    mes = ctk.CTkLabel(tela_relatorio, text="MÊS DO RELATÓRIO:")
    mes.pack(pady=10)
    mes_ = ctk.CTkOptionMenu(tela_relatorio, values=["JANEIRO", "FEVEREIRO", "MARCO", "ABRIL", "MAIO", "JUNHO",
                                                     "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"], width=150, height=30)
    mes_.pack(pady=10)

    # CONTATO DO RELATOR:
    contato = ctk.CTkLabel(tela_relatorio, text="CONTATO DO MARCADOR(A):")
    contato.pack(pady=10)
    contato_ = ctk.CTkEntry(tela_relatorio, width=400, height=25)
    contato_.pack(pady=10)

    # BOTÃO DE CONFIRMAÇÃO:
    botao_confirmar = ctk.CTkButton(tela_relatorio, text="GERAR RELATÓRIO", command=conf_relatorio, fg_color="#033A13")
    botao_confirmar.pack(pady=10)

    tela_relatorio.mainloop()

def conf_relatorio():
    # OBTENDO AS QUANTIDADES:
    global exames_relatorio
    global tela_relatorio
    global assinatura_, ano_, mes_, contato_
    global total, consultas, exames, cirurgias, resultados, medicamentos, relatorios, adulto, pediatrico
    total = len(exames_relatorio)
    consultas = len(exames_relatorio[exames_relatorio['PROCEDIMENTO'].str.contains('CONSULTA', na=False)])
    exames = len(exames_relatorio[exames_relatorio['PROCEDIMENTO'].str.contains('EXAME')])
    cirurgias = len(exames_relatorio[exames_relatorio['PROCEDIMENTO'].str.contains('CIRURGIA')])
    resultados = len(exames_relatorio[exames_relatorio['PROCEDIMENTO'].str.contains('RESULTADO')])
    medicamentos = len(exames_relatorio[exames_relatorio['PROCEDIMENTO'].str.contains('MEDICAMENTO')])
    relatorios = len(exames_relatorio[exames_relatorio['PROCEDIMENTO'].str.contains('RELATÓRIO')])
    adulto = len(exames_relatorio[~exames_relatorio['PROCEDIMENTO'].str.contains('PEDIÁTRICO', na=False)])
    pediatrico = len(exames_relatorio[exames_relatorio['PROCEDIMENTO'].str.contains('PEDIÁTRICO', na=False)])

    # INFORMAÇÕES DA TELA DE RELATÓRIO:
    municipio = cidade_.get().strip().title()
    assinatura = assinatura_.get().strip().title()
    contato_marcador = contato_.get().strip()
    ano_relatorio = ano_.get().strip()
    mes_relatorio = mes_.get().strip()

    # TELA DE CARREGAMENTO:
    loading = ctk.CTkToplevel(tela_relatorio)  # ou app, se preferir
    loading.title("CARREGANDO...")
    loading.geometry('400x150')
    ctk.CTkLabel(loading, text="GERANDO RELATÓRIO...", font=("Arial", 18)).pack(pady=30)
    loading.grab_set()
    loading.update_idletasks()

    def trabalho():
        global exames_relatorio
        # VERIFICANDO POSSIVEIS PROBLEMAS:
        try:    
            if not assinatura_.get().strip() or not ano_.get().strip() or not mes_.get().strip():
                raise Exception("Preencha todos os campos!")
            if exames_relatorio.empty:
                raise Exception("Base de dados vazia! Adicione pacientes antes de gerar o relatório.")
            if ano_.get().strip() not in [str(a) for a in range(2022, 2036)]:
                raise Exception("Ano inválido! Verifique o ano digitado.")

            # --- TABELAS ---

            # -> TABELA DAS INSTITUIÇÕES:

            # CONVERTENDO DATAFRAME EM LISTA:
            df_inst_ = exames_relatorio['INSTITUIÇÃO'].value_counts().reset_index()
            df_inst_.columns = ['Instituição', 'Total']
            df_inst = [df_inst_.columns.tolist()] + df_inst_.values.tolist()

            # CRIANDO TABELA:
            tabela = Table(df_inst, colWidths=[250, 100])
            tabela.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))

            exames_relatorio_pdf = [exames_relatorio.columns.tolist()] + exames_relatorio.values.tolist()

            # -> TABELA GERAL (PACIENTES):

            # CRIANDO STYLE:
            style_cell = ParagraphStyle(
                name='TabelaNormal',
                fontSize=8,
                leading=10,
                alignment=1,
                spaceBefore=0,
                spaceAfter=0
            )

            tabela_dados = [
                [Paragraph(str(cell), style_cell) for cell in row]
                for row in exames_relatorio_pdf
            ]
            # CONFIGURANDO TABELA:
            tabela_totais = LongTable(tabela_dados, colWidths=[120.9, 59.055, 111.6, 93.0, 79.98, 93.0])
            tabela_totais.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,1), (-1,-1), 8),
                ('FONTSIZE', (0,0), (-1,0), 9),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))

            # -> TABELA DOS PROCEDIMENTOS:

            procedimentos_data = {
                'Procedimento': ['Consulta', 'Exame', 'Cirurgia', 'Resultado', 'Medicamento', 'Retorno'],
                'Total': [consultas, exames, cirurgias, resultados, medicamentos, relatorios]
            }

            # CONVERTENDO EM DATAFRAME:
            df_procedimentos = pd.DataFrame(procedimentos_data)

            # CONVERTENDO EM LISTA DE LISTAS
            df_procedimentos = [df_procedimentos.columns.tolist()] + df_procedimentos.values.tolist()

            # CRIANDO TABELA:
            tabela_proc = Table(df_procedimentos, colWidths=[105, 50])
            tabela_proc.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))

            # TABELA PEDIATRIA/ADULTO:

            idade_data = {
                'Tipo': ['Adulto', 'Pediátrico'],
                'Total': [adulto, pediatrico]
            }

            # CRIANDO DATAFRAME:
            df_idade = pd.DataFrame(idade_data)

            # CCONVERTENDO EM LISTAS DE LISTAS
            df_idade = [df_idade.columns.tolist()] + df_idade.values.tolist()

            # CRIANDO TABELA
            tabela_idade = Table(df_idade, colWidths=[110, 70])
            tabela_idade.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))

            # -> TABELA DAS CONSULTAS:

            # FILTRANDO AS CONSULTAS:
            df_consultas = exames_relatorio[exames_relatorio['PROCEDIMENTO'].str.contains('CONSULTA', na=False)]
            contagem_especialidades = df_consultas['PROCEDIMENTO'].value_counts()
            df_top5_consultas = contagem_especialidades.head(5).reset_index()
            df_top5_consultas.columns = ['Especialidade', 'Total']

            # CRIANDO A TABELA:
            tabela_top5_data = [df_top5_consultas.columns.tolist()] + df_top5_consultas.values.tolist()
            tabela_top5 = Table(tabela_top5_data, colWidths=[250, 100])
            tabela_top5.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))

            # --- CONFIGURANDO O PDF ---

            # Configurações iniciais
            elementos = []
            doc = SimpleDocTemplate(f"Relatorio_{mes_.get()}.pdf", pagesize=A4)
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(
                name='JustifiedBodyText',
                parent=styles['BodyText'],
                alignment=TA_JUSTIFY,
                spaceAfter=12,
                leading=14,
            ))
            styles.add(ParagraphStyle(
                name='CenteredHeading1',
                parent=styles['Heading1'],
                alignment=TA_CENTER,
            ))
            largura_pagina, altura_pagina = A4


            # TEXTOS DO PDF:
            texto_1 = f"""
            O presente relatório tem como objetivo apresentar um resumo das atividades realizadas pela Central de Regulação de Exames e Consultas 
            do município de {municipio} durante o mês de {mes_.get()} de {ano_.get().strip()}. Este documento visa fornecer uma visão geral dos procedimentos realizados, 
            destacando os principais dados e estatísticas relevantes, para a gestão da saúde pública local. Durante o mês em questão, o marcador(a) 
            {assinatura} foi responsável por agendar um total de {total} procedimentos, incluindo consultas médicas e exames diversos. Dos procedimentos
            agendados, {adulto} foram para adultos, e {pediatrico} na categoria pediatria. 
            """
            texto_2 = f'''
            O trabalho em questão envolveu a coordenação eficiente dos recursos disponíveis durante o agendamento de cada procedimento, garantindo que
            os pacientes tivessem acesso oportuno aos serviços de saúde necessários. No total, foram realizadas {consultas} consultas, {exames} exames, {cirurgias} cirurgias, {resultados} resultados 
            de exames, {medicamentos} prescrições de medicamentos e {relatorios} retornos de procedimentos gerados.
            '''

            especialidades_list = (
                df_top5_consultas['Especialidade']
                .str.replace(r'^CONSULTA:\s*', '', regex=True)
                .str.replace(r'\s*-\s*.*$', '', regex=True)
                .tolist()
            )

            if len(especialidades_list) > 1:
                especialidades_txt = ', '.join(especialidades_list[:-1]) + f" e {especialidades_list[-1]}"
            elif especialidades_list:
                especialidades_txt = especialidades_list[0]
            else:
                especialidades_txt = ''

            texto_3 = f"""
            No que diz respeito às especialidades médicas mais demandadas no período, observou-se uma concentração significativa de atendimento 
            em áreas específicas. As especialidades com maior número de consultas agendadas foram: {especialidades_txt}, refletindo as principais
            necessidades assistenciais da população atendida. Esses dados são essenciais para o planejamento estratégico da rede de saúde, possibilitando
            uma melhor alocação de recursos e priorização dos atendimentos conforme a demanda observada.
            """

            texto_4 = f'''Dessa forma, para concluir a prestação de informações a Secretatia Municipal de Sáude de {municipio} sobre os agendamentos realizados
            pelo(a) a gente regulador(a) hambulatorial {assinatura}, estão dispostas a seguir todas as informações sobre as datas, horários, nomes, e observações
            a respeito dos agendamentos no mês de {mes_relatorio}.
            
            '''

            # ADICIONANDO OS ITENS AO PDF, ATRAVEZ DA LISTA ELEMENTOS:

            elementos.append(Spacer(5, 12))
            elementos.append(Paragraph(f"PREFEITURA MUNICIPAL DE {municipio.upper()}", styles['Normal']))
            elementos.append(Paragraph("SECRETARIA MUNICIPAL DE SAÚDE", styles['Normal']))
            elementos.append(Paragraph("CENTRAL DE MARCAÇÃO (CDM)", styles['Normal']))
            elementos.append(Paragraph(f"REGULADOR(a) AMBULATORIAL/MARCADOR(a): {assinatura}", styles['Normal']))
            elementos.append(Paragraph(f"CONTATO: {contato_marcador}", styles['Normal']))
            elementos.append(Spacer(5, 12))
            elementos.append(Paragraph(f"RELATÓRIO DE MARCAÇÕES - {mes_relatorio} / {ano_relatorio}", styles['CenteredHeading1']))
            elementos.append(Spacer(5, 12))
            elementos.append(Paragraph(texto_1, styles['JustifiedBodyText']))
            elementos.append(Spacer(1, 12))
            elementos.append(tabela_idade)
            elementos.append(Spacer(1, 12))
            elementos.append(Paragraph(texto_2, styles['JustifiedBodyText']))
            elementos.append(Spacer(1, 12))
            elementos.append(tabela_proc)
            elementos.append(Spacer(1, 12))
            elementos.append(Paragraph(texto_3, styles['JustifiedBodyText']))
            elementos.append(Spacer(1, 12))
            elementos.append(tabela_top5)
            elementos.append(Spacer(1, 12))
            elementos.append(Paragraph(texto_4, styles['JustifiedBodyText']))
            elementos.append(Spacer(1, 12))
            elementos.append(tabela_totais)
            elementos.append(Spacer(5, 12))
            elementos.append(PageBreak())
            elementos.append(Paragraph("Relatório gerado por sistema informatizado de agendamento de exames e consultas.", styles['Italic']))
            elementos.append(Paragraph(f"Assinado por {assinatura}", styles['Italic']))
            elementos.append(Paragraph("Regulador(a) Ambulatorial / Marcador(a)", styles['Italic']))

            relatorio_pdf = SimpleDocTemplate(f"Relatorio_{mes_.get()}_{ano_.get()}.pdf", pagesize=A4)
            relatorio_pdf.build(elementos)

            # FECHANDO AS JANELAS:
            loading.after(0, loading.destroy)
            tela_relatorio.after(0, _msg_sucesso)

        except Exception as e:
            tela_relatorio.after(100, lambda e=e: _msg_erro(str(e)))

    # MENSAGEM DE SUCESSO:
    def _msg_sucesso():
        ok = ctk.CTkToplevel(tela_relatorio)
        ok.title("SUCESSO"); ok.geometry('420x150')
        ctk.CTkLabel(ok, text=f"Relatório {mes_.get()} criado com sucesso!", font=("Arial", 16)).pack(pady=20)
        ctk.CTkButton(ok, text="OK", command=ok.destroy).pack(pady=10)

    # MENSAGEM DE ERRO:
    def _msg_erro(msg):
        err = ctk.CTkToplevel(tela_relatorio)
        err.title("ERRO"); err.geometry('500x220')
        ctk.CTkLabel(err, text=msg, font=("Arial", 14)).pack(padx=20, pady=20)
        ctk.CTkButton(err, text="OK", command=err.destroy).pack(pady=10)

    loading.destroy()
    threading.Thread(target=trabalho, daemon=True).start()
    return

def doubts():
    #CRIANDO JANELA:
    tela_duvidas = ctk.CTk()
    tela_duvidas.title("DÚVIDAS")
    tela_duvidas.geometry('950x500')

    #TEXTOS DAS DÚVIDAS:

    duvidas_texto = """
    DUVIDAS FREQUÊNTES:

    1. Como adicionar um paciente?
       - Preencha todos os campos no formulário e clique em "SALVAR".

       

    2. Como visualizar a base de dados?
       - Clique no botão "VIZUALIZAR BASE DE DADOS" para abrir a janela com a tabela.

       
    3. Como abrir um relatório existente?
       - Vá no botão "ABRIR RELATÓRIO" e selecione o arquivo EXCEL desejado! Assim você poderá continuar
         o relatório, adicionando mais pacientes.
    
       
    4. Como salvar os dados digitados?
       - Clique em "SALVAR OS DADOS" após preencher todos os campos do formulário, o aquivo será salvo
        automaticamente na pasta do programa, em formato EXCEL!
    
    
    5. Como gerar um relatório?
       - Clique em "GERAR RELATÓRIO", preencha os campos necessários e confirme.

       

    6. Como excluir um paciente?
       - Clique em "EXCLUIR", digite o nome completo do paciente e confirme.
       - Se você digitou o mesmo paciente duas vezes, o programa irá excluir o último adicionado.

       

    6. O que fazer se encontrar um erro?
       - Verifique as mensagens de erro exibidas e corrija os dados conforme necessário.

       

    7. Quais hospitais são aceitos?

    - Hospital Santa Isabel
    - Hospital Irmã Dulce Ribeira
    - Hospital da Mulher
    - Hospital Agenor Paiva
    - Hospital Couto Maia
    - CIMEB
    - Hospital Manoel Vitorino
    - Hospital Professor Edgar Santos
    - Ambulatório Magalhães Neto
    - Hospital Ana Nery
    - Hospital Otávio Mangabeira
    - Hospital Aristides Maltês
    - Hospital da Bahia
    - Hospital 2 de Julho
    - Hospital Professor Carvalho Luz
    - Hospital Mário Leal
    - Maternidade Professor José Maria de Magalhães Neto
    - CEDAR
    - Hospital Geral Ernesto Simões
    - HGE
    - Hospital Geral Roberto Santos
    - Hospital Santa Luzia
    - Hospital Português
    - Hospital Juliano Moreira
    - CEDAP 02
    - Hospital Irmã Dulce Patamares
    - Hospital do Homem Monte Serrá
    - Faculdade ZARN
    - Faculdade FTC
    - ADAB Baiana
    - CEDAF UFBA
    - CEPRED
    - CEDEBA
    - APAE
    - HEMOBA
    - IBOPC
    - Hospital do Suburbio
    - Hospital Couto Maia
    - Clínica AFAC
    - Clínica Histocito Biopsias
    - Hospital Municipal
    - Hospital Metropolitano
    - Faculdade Unijorge
    - Multi Centro Carlos Gomes
    - Faculdade de Odontologia da UFBA
    - CICAM
    - HISTOCITO
    - Martagão Gesteira
    - IOBA
    - CDTO
    - ICS UFBA
    - DULCIMED
    - Instituto dos Cegos da Bahia
    - Maternidade Climério de Oliveira
    - HOEB
    - Hospital Eládio
    


    8. Quais tipos de consultas são aceitos?

    - Otorrinolaringologista
    - Reumatologista
    - Cardiologista
    - Hematologista
    - Cabeça E Pescoço
    - Pneumologista
    - Cirurgião Torácico
    - Gastro
    - Hepatologista
    - Endocrinologista
    - Bucomaxilo
    - Triagem Oncológica
    - Urologista
    - Ginecologista
    - Mastologista
    - Neurologista
    - Neurocirurgião
    - Clínica Da Dor
    - Ambulatório Do Sono
    - Cirurgião Pediátrico
    - Alergologista
    - Oftalmologista
    - Neuro Oftalmo
    - Ortopedista
    - Clínica Da Obesidade
    - Cirurgião Vascular
    - Cirurgião Geral
    - Estomatologista
    - Anestesista
    - Nutricionista
    - Enfermagem
    - Serviço Social
    - PAPO
    - Angiologista
    - Nefrologista
    - Coloproctologista
    - Dermatologista
    - Psicólogo
    - Psiquiatra
    - Fonoaudiólogo
    - Fisioterapeuta
    - Terapeuta Ocupacional
    - Odontopediatra
    - Dentista
    - Pediatra
    - Infectologista
    - Geriatra
    - Cirurgião Bucomaxilo
    - Cirurgião Plástico
    - Cirurgião Vascular
    - Cirurgião Torácico
    - Pneumologista
    - Cirurgião Plástico
    - Obstetra
    - Geneticista
    - Ambulatório Trans
    - Odontologista
    - Dentista
    - Hipertensão Pulmonar
    - Cirurgia Bariátrica
    - Ambulatório Do Adolescente
    - Onco Emato
    - Imunologista



    9. Quem devo contatar para mais ajuda?

       - Em caso de dúvidas adicionais, entre em contato com o desenvolvedor do sistema
       de relatórios, Handrick Silveira, através do número: 71992595917

    """

    # PONDO EM UM SCROLLLABEL
    scrollable_frame_d = ctk.CTkScrollableFrame(tela_duvidas, width=580, height=380)
    scrollable_frame_d.pack(padx=20, pady=20, fill="both", expand=True)
    label_duvidas = ctk.CTkLabel(scrollable_frame_d, text=duvidas_texto, justify=tk.LEFT, font=("Arial", 20))
    label_duvidas.pack()
    tela_duvidas.mainloop()

def save_relatorio():
    global exames_relatorio, tela_save_relatorio

    #TELA DE CONFIRMAÇÃO DE SALVAMENTO:
    tela_save_relatorio = ctk.CTkToplevel(app)
    tela_save_relatorio.title("Salvar Relatório")
    tela_save_relatorio.geometry("650x250")
    tela_save_relatorio.grab_set()

    #LABEL PRA CONFIRMAÇÃO:
    confirmacao = ctk.CTkLabel(tela_save_relatorio, text="Tem certeza que quer salvar o relatório?\n\n O salvamento fará com que você não perca as informações caso\no programa seja fechado, podendo ser continuado posteriormente.", font=("Arial", 19))
    confirmacao.pack(padx=10, pady=10)

    #BOTÃO DE CONFIRMAÇÃO:
    botao_confirmar = ctk.CTkButton(tela_save_relatorio, text="CONFIRMAR", command=conf_salvar_relatorio, fg_color="#0c2d46", hover_color="#1B1342")
    botao_confirmar.pack(padx=10, pady=10)

def conf_salvar_relatorio():
    global exames_relatorio, tela_save_relatorio
    exames_relatorio.to_excel("Relatório de Exames (Incompleto).xlsx", index=False)
    tela_save_relatorio.destroy()
    # TELA DE SUCESSO:
    tela_sucesso = ctk.CTk()
    tela_sucesso.title("SUCESSO")
    tela_sucesso.geometry("300x100")
    sucesso = ctk.CTkLabel(tela_sucesso, text="Relatório salvo com sucesso!", font=("Arial", 16))
    sucesso.pack(padx=10, pady=10)
    tela_sucesso.mainloop()

def selecionar_arquivo():
    global exames_relatorio, lista_colunas

    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo Excel",
        filetypes=[("Arquivos Excel", "*.xlsx")]
    )
    if not caminho_arquivo:
        return

    try:
        df = pd.read_excel(caminho_arquivo)

        if set(df.columns) != set(lista_colunas):
            raise ValueError("Colunas inválidas no arquivo")

        if exames_relatorio is not None and not exames_relatorio.empty:
            raise RuntimeError("Já existe uma base carregada")

        exames_relatorio = df[lista_colunas]

        tela_relatori_upload = ctk.CTkToplevel()
        tela_relatori_upload.title("SUCESSO")
        tela_relatori_upload.geometry("500x150")
        ctk.CTkLabel(tela_relatori_upload, text="Arquivo carregado com sucesso!", font=("Arial", 18)).pack(padx=10, pady=10)
        tela_relatori_upload.grab_set()
        tela_relatori_upload.focus_force()
        tela_relatori_upload.lift() 
    except Exception as e:
        tela_erro_upload = ctk.CTkToplevel()
        tela_erro_upload.title("ERRO")
        tela_erro_upload.geometry("630x250")
        msg1 = "Erro ao carregar o arquivo:\n\n"
        msg2 = f"{str(e)}\n\n(Se já existirem pacientes digitalizados, reinicie o programa e tente novamente)"
        ctk.CTkLabel(tela_erro_upload, text=msg1, font=("Arial", 20)).pack(padx=10, pady=10)
        ctk.CTkLabel(tela_erro_upload, text=msg2, font=("Arial", 16)).pack(padx=10, pady=5)
        tela_erro_upload.grab_set()
        tela_erro_upload.focus_force()
        tela_erro_upload.lift()

# ABA PRINCIPAL
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Exames")
app.geometry('1230x750')

# SCROLLBAR
scroll_frame = ctk.CTkScrollableFrame(app, width=350, height=350)
scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)

 # NOME DO PACIENTE:
nome = ctk.CTkLabel(scroll_frame, text="NOME DO PACIENTE:", font=("Arial", 13))
nome.pack()
nome_ = ctk.CTkEntry(scroll_frame, width=420, height=25)
nome_.pack(padx=10, pady=7)


# CONTADO DO PACIENTE:
tel = ctk.CTkLabel(scroll_frame, text="TELEFONE:", font=("Arial", 13))
tel.pack()
tel_ = ctk.CTkEntry(scroll_frame, width=420, height=25)
tel_.pack(padx=10, pady=7)

# PROCEDIMENTO:

proc = ctk.CTkLabel(scroll_frame, text="PROCEDIMENTO:", font=("Arial", 13))
proc.pack()

opcao_selecionada = tk.StringVar(value="")
procedimentos_possiveis = ctk.CTkSegmentedButton(scroll_frame, values=["CONSULTA", "EXAME", "RESULTADO",
                                        "CIRURGIA", "MEDICAMENTO", "RETORNO"], corner_radius=30,
                                        width=4600, height=48, variable=opcao_selecionada, selected_color="#2E1246", selected_hover_color="#2A0731")
procedimentos_possiveis.pack(padx=10, pady=7)

# DETALHAMENTO DO PROCEDIMENTO:
deta = ctk.CTkLabel(scroll_frame, text="DETALHAMENTO DO PROCEDIMENTO:", font=("Arial", 13)).pack(padx=0, pady=0)
deta_ = ctk.CTkEntry(scroll_frame, width=420, height=25)
deta_.pack(padx=25, pady=25)
consulta_frame = ctk.CTkFrame(scroll_frame , fg_color="lightgray")
consulta_frame.place_forget()
deta_.bind("<KeyRelease>", sugestao_consultas)



# ADULTO OU CRIANÇA:
adulto = ctk.CTkLabel(scroll_frame, text="ADULTO OU PEDIATRICO:", font=("Arial", 13))
adulto.pack(padx=0, pady=0)
adulto_ = ctk.CTkOptionMenu(scroll_frame, values=["ADULTO", "PEDIATRICO"], width=150, height=30, button_color="#5B2C77", fg_color="#5B2C77")
adulto_.pack(padx=10, pady=7)


# INSTITUIÇÃO:
inst = ctk.CTkLabel(scroll_frame, text="INSTITUIÇÃO:", font=("Arial", 13))
inst.pack(padx=0, pady=0)
inst_ = ctk.CTkEntry(scroll_frame, width=400, height=28)
inst_.pack(padx=10, pady=7)
inst_.bind("<KeyRelease>", sugestao_hospital)

suggestion_frame = ctk.CTkFrame(scroll_frame, fg_color="lightgray")
suggestion_frame.place_forget()


# DATA DO AGENDAMENTO:
data = ctk.CTkLabel(scroll_frame, text="DATA DO AGENDAMENTO/CAPITAÇÃO:", font=("Arial", 13))
data.pack(padx=0, pady=0)
data_ = ctk.CTkEntry(scroll_frame, width=100, height=30)
data_.pack(padx=10, pady=7)

# HORÁRIO DO AGENDAMENTO:

horario = ctk.CTkLabel(scroll_frame, text="HORÁRIO DO AGENDAMENTO:", font=("Arial", 13))
horario.pack(padx=0, pady=0)
horario_ = ctk.CTkEntry(scroll_frame, width=100, height=30)
horario_.pack(padx=10, pady=7)

# ENVIO:
env = ctk.CTkLabel(scroll_frame, text="ENVIO:", font=("Arial", 13))
env.pack(padx=0, pady=0)
env_ = ctk.CTkEntry(scroll_frame, width=360, height=28)
env_.pack(padx=10, pady=7)

# BOTÃO DE SALVAR:
save = ctk.CTkButton(scroll_frame, text="SALVAR", command=salvar, fg_color="#0c2d46", hover_color="#1B1342")
save.pack(padx=10, pady=10)

# BOTÃO DE LIMPAR:
clean = ctk.CTkButton(scroll_frame, text="LIMPAR", command=limpar, fg_color="#613d0e", hover_color="#272108")
clean.pack(padx=10, pady=10)

# BOTÃO DE EXCLUIR
delete = ctk.CTkButton(scroll_frame, text="EXCLUIR", command=excluir, fg_color="#470c14", hover_color="#2C0303")
delete.pack(padx=10, pady=10)

# BOTÃO DE VIZUALIZAÇÃO:
view = ctk.CTkButton(scroll_frame, text="VIZUALIZAR BASE DE DADOS", command=visualizar, fg_color="#887210", hover_color="#333206")
view.pack(padx=5, pady=5)

#ESPAÇAMENTO:
espaco = ctk.CTkLabel(scroll_frame, text="\n")
espaco.pack(padx=5, pady=5)

# BOTÃO DE RELATÓRIO:
report = ctk.CTkButton(scroll_frame, text="GERAR RELATÓRIO", command=relatorio, fg_color="#0a411f", hover_color="#0C2417")
report.pack(padx=5, pady=5)

#BOTÃO DE UPLOAD:
upload = ctk.CTkButton(scroll_frame, text="ABRIR RELATÓRIO", command=selecionar_arquivo, fg_color="#550e3a", hover_color="#350A23")
upload.pack(padx=5, pady=5)

# BOTÃO DE SALVAR DADOS:
save_rel = ctk.CTkButton(scroll_frame, text="SALVAR OS DADOS", command=save_relatorio, fg_color="#656621", hover_color="#4D5313")
save_rel.pack(padx=5, pady=5)
#BOTÃO DE DÚVIDAS:
duvidas = ctk.CTkButton(scroll_frame, text="DÚVIDAS?", command=doubts, fg_color= "#000000", hover_color="#000000")
duvidas.pack(padx=5, pady=5)

# LOOP DA TELA PRINCIPAL:
app.mainloop()