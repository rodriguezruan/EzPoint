import tkinter
import tkinter as tk
from tkinter import ttk, Tk, messagebox

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import bcrypt
from bcrypt import checkpw

from PIL import Image, ImageTk

from tkinterhtml import HtmlFrame

import webbrowser

# Autenticação firestore -------------------

cred = credentials.Certificate('ezpoint-cd326-firebase-adminsdk-6yfjv-7e14cc16f2.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

result = db.collection('Funcionarios').document("users").get()


# CORES -------------------------------------

co1 = "#feffff" # BRANCA
co2 = "#23d083" # VERDE/AZUL
co3 = "#f4fb98" # AMARELO
co4 = "#0e0f0f" # PRETO
co5 = "#177e50" # VERDE/AZUL ESCURO

# Variavel teste ----------------------------

x=0

validacao_var = ""

infoepi_frame = None

senha_visivel=False
senha_input = None

#olho_aberto = None
#olho_fechado = None


# ------------------------------ FUNÇÃO REGISTER ---------------------------------


def register():
    #global olho_aberto, olho_fechado

    j.withdraw() # Oculta a janela

# Modifique a função do botão "Voltar ao Menu" para chamar a função limpar_tela

    def voltar_ao_menu():
        global validacao_var
        validacao_var = ""
        window.destroy() 
        j.deiconify()  # Mostrar a tela do menu principal novamente


    
    # CARACTERIZANDO A PÁGINA -------------------
    window = Tk()
    window.title("Register")
    window.geometry('625x680')
    window.configure(bg=co1)
    window.resizable(width=False, height=True) # Isso faz com que a janela aumente ou nao

    #olho_aberto = ImageTk.PhotoImage(Image.open("eye.png"))
    #olho_fechado = ImageTk.PhotoImage(Image.open("eye-off.png"))

    # DIVIDINDO A TELA --------------------------

    frame_cima = tkinter.Frame(window, width=600, height=50, bg=co1, relief='flat')
    frame_cima.grid(row=0, column=0, padx=0, pady=1, sticky='nsew')

    frame_baixo = tkinter.Frame(window, width=600, height=350, bg=co1, relief='flat') 
    frame_baixo.grid(row=1, column=0, padx=0, pady=1, sticky='news')


    

    # TITULO ------------------------------------

    l_nome = tkinter.Label(frame_cima, text = 'REGISTRO', anchor='ne', font=('Ivy 25'), bg=co1, fg=co4)
    l_nome.place(x=5,y=5)

    l_linha = tkinter.Label(frame_cima, text = '', width=585, anchor='nw', font=('Ivy 1'), bg=co2, fg=co4)
    l_linha.place(x=10,y=45)


    # FUNÇÃO DE MENSAGENS ----------------------------------    
    
    def enter_data():
        
        salt = bcrypt.gensalt()

        #print(validacao_var)
                
        if validacao_var == "Aceito":
            primeiro_nome = primeiro_nome_input.get()
            sobrenome = sobrenome_input.get()
            email = email_input.get()
            senha = senha_input.get()
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
            id = id_input.get()
                    
            if primeiro_nome and sobrenome and email and senha and id:
                cargo = cargo_combobox.get()
                sexo = sexo_combobox.get()

                if cargo == 'Produção Química' or cargo == 'Surpervisor' or cargo == 'Soldador' or cargo == '' or cargo == 'Produção':
                    if sexo == 'Femino' or sexo == 'Masculino' or sexo == 'Prefiro não dizer':               

                        result = db.collection('Funcionarios').where('email', '==', email).get()

                        if len(result) == 0:
                            fire = {
                                "nome": primeiro_nome,
                                "sobrenome": sobrenome,
                                "cargo": cargo,
                                "sexo": sexo,
                                "email": email,
                                "senha": senha_hash
                            }

                            doc_ref = db.collection("Funcionarios").document(id)
                            doc_ref.set(fire)

                            tkinter.messagebox.showwarning(title="Sucesso", message="Registro feito com sucesso!!!")

                            primeiro_nome_input.delete(0,'end')
                            sobrenome_input.delete(0,'end')
                            email_input.delete(0,'end')
                            senha_input.delete(0,'end')
                            id_input.delete(0,'end')
                            sexo_combobox.delete(0,'end')
                            cargo_combobox.delete(0,'end')
                            if infoepi_frame:
                                infoepi_frame.destroy()
                            termos_check.deselect()
                        else:
                            tkinter.messagebox.showwarning(title="Erro", message="Usuário já existente")
                    else:
                        tkinter.messagebox.showwarning(title="Erro", message='Selecione as opções de genero dadas!')
                else:
                    tkinter.messagebox.showwarning(title='Erro', message='Selecione as opções de áreas de atuação dadas!')          
            else:
                tkinter.messagebox.showwarning(title="Ocorreu um erro", message="Preencha todos os campos obrigatórios")
        else:
            tkinter.messagebox.showwarning(title="Ocorreu um erro", message="Você não aceitou os termos da empresa")


    # FUNÇAO EPIS -----------------------------------------


    def epi2() : # Função deu certo
        
        #print("dentro do epi 2")

        global infoepi_frame   # Acessar a variável global
    
        if infoepi_frame:  # Destruir o widget anterior, se existir
            infoepi_frame.destroy()

        infoepi_frame = tk.LabelFrame(frame_baixo, text="Equipamentos Necessários:", bg=co1, fg=co4, font=('Ivy 10 bold'))
        infoepi_frame.grid(row=2, column=0, padx=20, pady=10)

        cargo = cargo_combobox.get()


        if cargo == "Produção": 
            epi_produ = tkinter.Label(infoepi_frame, text="""-> Protetor Auditivo\n       -> Óculos de Segurança\n           -> Capacete de Segurança\n    -> Luvas de Segurança\n -> Botas de Proteção\n              -> Máscaras ou Respiradores""", bg=co1, fg=co4, font=('Ivy 8'))
            epi_produ.grid(row=0, column=2, padx=25)
        
        elif cargo == "":
            epi_produ = tkinter.Label(infoepi_frame, text="-> Selecione algum cargo ", bg=co1, fg=co4, font=('Ivy 8 bold'))
            epi_produ.grid(row=0, column=2, padx=62)
        
        elif cargo == "Soldador":
            epi_produ = tkinter.Label(infoepi_frame, text="""    -> Luvas de Segurança\n-> Protetor Auditivo\n-> Avental de Raspa\n                  -> Calçado de Segurança          \n    -> Óculos de Proteção\n                        -> Respirador de Soldagem            """, bg=co1, fg=co4, font=('Ivy 8'))
            epi_produ.grid(row=0, column=2)
        
        elif cargo == "Supervisor":       
            epi_produ = tkinter.Label(infoepi_frame, text="""-> Capacetes\n                   -> Coletes de Segurança\n                -> Óculos de Proteção""", bg=co1, fg=co4, font=('Ivy 8'))
            epi_produ.grid(row=0, column=2, padx=30)
        
        elif cargo == "Produção Química":        
            epi_produ = tkinter.Label(infoepi_frame, text="""-> Luvas Laboratoriais\n      -> Aventais de Segurança\n           -> Máscaras ou Respiradores\n-> Óculos de Proteção\n  -> Macacões Químicos\n                  -> Toucas para Segurar o Cabelo""", bg=co1, fg=co4, font=('Ivy 8'))
            epi_produ.grid(row=0, column=2, padx=10)
        else:
            epi_produ = tkinter.Label(infoepi_frame, text='Por favor, selecione umas das opções!', bg=co1, fg=co4, font=('Ivy 8'))
            epi_produ.grid(row=0, column=2, padx=30)



    #------------------------------------------------1ª PARTE------------------------------------------------

    # TITULO ------------------------------------

    infouser_frame = tkinter.LabelFrame(frame_baixo, text="Informações Pessoais", bg=co1, fg=co4, font=('Ivy 10 bold'))
    infouser_frame.grid(row=0, column=0, padx=20, pady=10)

    # INSERIR O NOME E SOBRENOME ----------------

    primeiro_nome = tkinter.Label(infouser_frame, text="Nome *", bg=co1, fg=co4, font=('Ivy 9 bold'))
    primeiro_nome.grid(row=0, column=0)
    sobrenome = tkinter.Label(infouser_frame, text="Sobrenome *", bg=co1, fg=co4, font=('Ivy 9 bold'))
    sobrenome.grid(row=0, column=1)
    primeiro_nome_input = tkinter.Entry(infouser_frame, font=("",10), highlightthickness=1, relief='solid')
    sobrenome_input = tkinter.Entry(infouser_frame, font=("",10), highlightthickness=1, relief='solid')
    primeiro_nome_input.grid(row=1, column=0)
    sobrenome_input.grid(row=1, column=1)

    # INSERIR O SEXO ----------------------------

    sexo = tkinter.Label(infouser_frame, text="Gênero", bg=co1, fg=co4, font=('Ivy 9 bold'))
    sexo_combobox = ttk.Combobox(infouser_frame,values=[ "", "Feminino", "Masculino", "Prefiro não dizer"])
    sexo.grid(row=0, column=2)
    sexo_combobox.grid(row=1, column=2)


    # INSERIR SENHA E EMAIL --------------------

    email = tkinter.Label(infouser_frame, text="Email *", bg=co1, fg=co4, font=('Ivy 9 bold'))
    email.grid(row=2, column=0)
    senha = tkinter.Label(infouser_frame, text="Senha *", bg=co1, fg=co4, font=('Ivy 9 bold'))
    senha.grid(row=2, column=1)

    atencao1 = tkinter.Label(infouser_frame, text="* OBS.:", bg=co1, fg=co2, font=('Ivy 8 bold'))
    atencao1.grid(row=4, column=0)

    atencao2 = tk.Label(infouser_frame, text=' A senha não é obrigatóriamente a do email, você a usará em seu login!', bg=co1, fg=co2, font=('Ivy 8 bold'))
    atencao2.grid(row=5, column=0, columnspan=2)

    email_input = tkinter.Entry(infouser_frame, font=("",10), highlightthickness=1, relief='solid')
    email_input.grid(row=3, column=0)
    senha_input = tkinter.Entry(infouser_frame, show="*", font=("",10), highlightthickness=1, relief='solid')
    senha_input.grid(row=3, column=1)


    # Função para alternar entre ocultar e mostrar a senha
    """ def alternar_senha():
        global senha_input, senha_visivel
        if senha_visivel:
            senha_input["show"] = "*"
            senha_visivel = False
            ver_imagem.config(image=olho_fechado)
        else:
            senha_input["show"] = ""
            senha_visivel = True
            ver_imagem.config(image=olho_aberto) """ 
    
    def alternar_senha():
        if senha_input.cget("show") == "*":
            senha_input.config(show="")
            ver_imagem.config(text="Ocultar Senha")
        else:
            senha_input.config(show="*")
            ver_imagem.config(text="Mostrar Senha")


    ver_imagem = tk.Button(infouser_frame, text="Mostrar senha", command=alternar_senha, bg=co1,fg=co4, font=("Ivy 8"))
    ver_imagem.grid(row=4, column=1)
    
    # INSERIR ID CARTERINHA --------------------

    nom_id = tk.Label(infouser_frame, text="ID do Cartão *", bg=co1, fg=co4, font=('Ivy 9 bold'))
    nom_id.grid(row=2, column=2)

    id_input = tk.Entry(infouser_frame, font=("",10), highlightthickness=1, relief='solid')
    id_input.grid(row=3, column=2)

    #Para todos os capos de informação de usuário, ele adiciona um espaçamento -------------

    for widget in infouser_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)



    #------------------------------------------------2ª PARTE------------------------------------------------

    # TITULO ------------------------------------

    infojob_frame = tkinter.LabelFrame(frame_baixo, text="Ocupação no Trabalho", bg=co1, fg=co4, font=('Ivy 10 bold'))
    infojob_frame.grid(row=1, column=0, padx=20, pady=10)

    # CARGO -------------------------------------

    cargo = tkinter.Label(infojob_frame, text="Área de atuação", bg=co1, fg=co4, font=('Ivy 9 bold'))
    cargo_combobox = ttk.Combobox(infojob_frame,values=[ "", "Produção", "Supervisor", "Produção Química", "Soldador"])
    cargo.grid(row=1, column=0)
    cargo_combobox.grid(row=2, column=0)


    botao = tkinter.Button(infojob_frame, text="Saber EPIs", command= epi2, font=('Ivy 9'), bg=co2, fg=co4) # Pode mudar a funçao
    botao.grid(row=2, column=1, sticky="news", padx=20, pady=20)

    # Adiciona um espaçamento -------------------

    for widget in infojob_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)



    #------------------------------------------------3ª PARTE------------------------------------------------

    # TERMOS E CONDIÇÕES ------------------------

    def teste():
        global x, validacao_var

        x += 1

        if x == 1:
            validacao_var = "Aceito"
            #print("Clicou no aceito: ", validacao_var)
        else:
            x = 0
            validacao_var = "Nao Aceito"
            #print("Clicou no nao aceito: ", validacao_var)
       
        return validacao_var
    
    global x
    x = 0
    

    termos_frame = tkinter.LabelFrame(frame_baixo, text="Termos e Condições *", bg=co1, fg=co4, font=('Ivy 10 bold'))
    termos_frame.grid(row=3, column=0, sticky="news")

    # JANELA DE TERMOS E CONDIÇÕES ---------------------------------

    def abrir_termos_condicoes():
    # Aqui você pode abrir uma nova janela ou fazer qualquer outra ação
    # quando o link for clicado
        print("Abrindo os termos e condições...")

    # Abra o arquivo HTML em um navegador externo (substitua 'seuarquivo.html' pelo caminho do seu arquivo HTML)
        arquivo_html = "TC.html"
        webbrowser.open_new_tab(arquivo_html)



# Cria o link com a frase ------------------------------

    texto_link = "termos e condições"
    link_label = tk.Label(termos_frame, text=texto_link, cursor="hand2", fg="blue", font=("Ivy 9 bold"), bg=co1)
    link_label.grid(row=0, column=1, sticky="w")
    link_label.bind("<Button-1>", lambda event: abrir_termos_condicoes())

# Check -------------------------------------------------

    termos_check = tkinter.Checkbutton(termos_frame, text="Eu aceito os", variable=validacao_var, bg=co1, fg=co4, font=('Ivy 9 bold'), command=teste)
    termos_check.grid(row=0, column=0, sticky="w")

    

    #------------------------------------------------4ª PARTE------------------------------------------------
    
    
    # BOTÃO DE REGISTRO -------------------------

    botao = tkinter.Button(frame_baixo, text="Registrar", command= enter_data, font=('Ivy 10 bold'), bg=co2, fg=co4)
    botao.grid(row=4, column=0, sticky="news", padx=10, pady=5)

    menu = tkinter.Button(frame_baixo, text = 'Voltar ao Menu', command = voltar_ao_menu, font=('Ivy 10 bold'), bg=co2, fg=co4)
    menu.grid(row=5, column=0, sticky='news', padx=10, pady=5)

    

    #print(".")

    window.mainloop()
    

# ------------------------------ FUNÇÃO LOGIN ---------------------------------

def login():

    j.withdraw() # Oculta a janela

    def voltar_ao_menu():
        j.deiconify() # Mostra dnv a janela
        window.destroy()

# CARACTERIZANDO A PÁGINA -------------------

    window = Tk()
    window.title("Login")
    window.geometry('340x270')
    window.configure(bg=co1)
    window.resizable(width=False, height=False)

# DIVIDINDO A TELA --------------------------

    frame_cima = tkinter.Frame(window, width=400, height=60, bg=co1, relief='flat')
    frame_cima.grid(row=0, column=0, padx=0, pady=1, sticky='nsew')

    frame_baixo = tkinter.Frame(window, width=400, height=250, bg=co1, relief='flat')
    frame_baixo.grid(row=1, column=0, padx=0, pady=1, sticky='news')

# TITULO ------------------------------------

    l_nome = tkinter.Label(frame_cima, text = 'LOGIN', anchor='ne', font=('Ivy 25'), bg=co1, fg=co4)
    l_nome.place(x=5,y=5)

    l_linha = tkinter.Label(frame_cima, text = '', width=310, anchor='nw', font=('Ivy 1'), bg=co2, fg=co4)
    l_linha.place(x=10,y=45)

# FUNCÕES DE VERIFICAÇÃO DE USUÁRIO ---------

    def confirmação():
        senha = senha_input.get()
        email = email_input.get()

        if senha and email :
       
            doc_ref = db.collection('Funcionarios').where('email', '==', email)
            docs = list(doc_ref.stream())  # Converter o gerador em uma lista

            if len(docs) == 0:
              tkinter.messagebox.showwarning(title="Erro", message="Usuário não encontrado!")
              return

            for doc in docs:
              hash_senha_firestore = doc.to_dict().get('senha')
              senha_usuario = senha_input.get()

              if checkpw(senha_usuario.encode('utf-8'), hash_senha_firestore):
                      tkinter.messagebox.showinfo(title="Sucesso", message="Logado com sucesso!")
                      return
              
              else:
                     tkinter.messagebox.showwarning(title="Erro", message="Senha ou email incorretos!")

 
        else:
            tkinter.messagebox.showwarning(title="Erro", message="É necessário completar todos os campos de informações!!")


#------------------------------------------------1ª PARTE------------------------------------------------


#------------------------------------------------2ª PARTE------------------------------------------------

# INSERIR A SENHA ---------------------------

    senha = tkinter.Label(frame_baixo, text="Senha", font=('Ivy 10 bold'), bg=co1, fg=co4)
    senha.grid(row=4, column=1,padx=0, pady=10)
    senha_input = tkinter.Entry(frame_baixo, justify='left', font=("",10), highlightthickness=1, relief='solid', show="*")
    senha_input.grid(row=5, column=0,padx=10, pady=1)

# INSERIR A EMAIL ----------------------------

    email = tkinter.Label(frame_baixo, text="Email", font=('Ivy 10 bold'), bg=co1, fg=co4)
    email.grid(row=4, column=0,padx=10, pady=10)
    email_input = tkinter.Entry(frame_baixo, justify='left', font=("",10), highlightthickness=1, relief='solid')
    email_input.grid(row=5, column=1,padx=10, pady=10)


#------------------------------------------------3ª PARTE------------------------------------------------

    vazio = tkinter.Label(frame_baixo, text='', bg=co1,fg=co1)
    vazio.grid(row=8, column=0,padx=0, pady=1)

# BOTÃO DE LOGIN -------------------------

    botao = tkinter.Button(frame_baixo, text="        Login         ", font=('Ivy 10 bold'), bg=co2, fg=co4, command=confirmação)
    botao.grid(row=10, column=0, columnspan=2, sticky="news", padx=10, pady=5)

    menu = tkinter.Button(frame_baixo, text="Voltar ao Menu", font=('Ivy 10 bold'), bg=co2, fg=co4, command = voltar_ao_menu)
    menu.grid(row=11, column=0,columnspan=2, sticky='news', padx=10, pady=5)
    


    window.mainloop()



# ---------------------------------------- MENU --------------------------------------

# CARATERIZANDO MENU ----------------------------------

j = Tk()
j.title('MENU')
j.geometry('650x300')
j.configure(bg=co1)
j.resizable(width=False, height=False)

# DIVIDINDO A TELA --------------------------

frame_cima = tkinter.Frame(j, width=700, height=80, bg=co3, relief='flat')
frame_cima.grid(row=0, column=0, padx=0, pady=1, sticky='nsew')

frame_baixo = tkinter.Frame(j, width=700, height=20, bg=co1, relief='flat')
frame_baixo.grid(row=1, column=0, padx=0, pady=1, sticky='nsew')

frame_bb = tkinter.Frame(j, width=700, height=20, bg=co1, relief='flat')
frame_bb.grid(row=2, column=0, padx=0, pady=1, sticky='nsew')

# Centralizando frame_bb verticalmente
j.grid_rowconfigure(2, weight=1)
j.grid_columnconfigure(0, weight=1)


# TITULO ------------------------------------

t_ez = tk.Label(frame_cima, text='Ez', anchor='n', font=('Ivy 45'), bg=co3, fg=co2)
t_ez.place(x=215,y=5)
t_po = tk.Label(frame_cima, text='Point', anchor='e', font=('Ivy 45'), bg=co3, fg=co5)
t_po.place(x=285,y=5)

# linha ----------------------------

l_linha = tkinter.Canvas(frame_cima, width=620, bg=co3, borderwidth=0, highlightthickness=0)
l_linha.place(x=10,y=70)

# Desenhando bolinhas no canvas ----

for x in range(5, 720, 30):
    l_linha.create_oval(x, 5, x + 15, 15, fill=co5, outline=co5)

# -------------------------------------------

l_linha = tkinter.Canvas(frame_baixo, width=620, bg=co1, borderwidth=0, highlightthickness=0)
l_linha.place(x=1,y=-10)

# Desenhando bolinhas no canvas ----

for x in range(-5, 720, 30):
    l_linha.create_oval(x, 5, x + 15, 15, fill=co2, outline=co2)

# FRASE --------------------------------------

fra = tk.Label(frame_bb, text='Bem-vindo(a)! Tenha um ótimo trabalho!\nSelecione a opção desejada.', bg=co1, fg=co4)
fra.grid(row=0, column=0, columnspan=2, pady=2)

# Centralizando os botões horizontalmente
frame_bb.grid_rowconfigure(1, weight=0)
frame_bb.grid_columnconfigure(0, weight=1)
frame_bb.grid_columnconfigure(1, weight=1)

# BOTÕES DE REG E LOG ------------------------

botao_re = tk.Button(frame_bb, text = 'Registrar', command = register, font=('Ivy 10 bold'),bg=co2,fg=co4)
botao_re.grid(row = 1, column = 0, pady=50, padx=(110,3))

botao_lo = tk.Button(frame_bb, text = 'Login', command = login, font=('Ivy 10 bold'),bg=co2,fg=co4)
botao_lo.grid(row = 1, column = 1, pady=50, padx=(3,120)) 


j.mainloop()
