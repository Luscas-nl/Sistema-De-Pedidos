from tkinter import *
from tkinter import font
from tkinter import ttk
import sqlite3

win = Tk()

class Funcs():
    def limparTela(self):
        self.enMesa.delete(0, END)
        self.strBeb.set("Bebida")
        self.strBurg.set("Hamburguer")
        self.enCod.delete(0, END)
    def conectaDb(self):
        self.con = sqlite3.connect("pedidos.db")
        self.cursor = self.con.cursor(); print("Banco de dados conectado")
    def desconectaDb(self):
        self.con.close(); print("Banco de dados desconectado")
    def criarTabela(self):
        self.conectaDb()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                cod INTEGER PRIMARY KEY,
                mesa INTEGER,
                burg CHAR(20) NOT NULL,
                beb CHAR(20) NOT NULL,
                valor INTEGER
            );
        """)
        self.con.commit(); print("Banco de dados criado")
        self.desconectaDb()
    def variaveis(self):
        self.mesa = self.enMesa.get()
        self.beb = self.strBeb.get().upper()
        self.burg = self.strBurg.get().upper()
        self.cod = self.enCod.get()
    def addPedido(self):
        self.variaveis()
        self.valor = self.valueBurg + self.valueBeb
        self.conectaDb()
        
        self.cursor.execute(""" INSERT INTO pedidos(mesa, burg, beb, valor) 
            VALUES (?, ?, ?, ?) """, (self.mesa, self.burg, self.beb, self.valor))
        self.con.commit()
        self.desconectaDb()
        self.selectPedido()
        self.limparTela()        
    def selectPedido(self):
        self.pedidos.delete(*self.pedidos.get_children())
        self.conectaDb()
        listaPedidos = self.cursor.execute(""" SELECT cod, mesa, burg, beb , valor FROM pedidos 
                                            ORDER BY cod ASC; """)
        
        for i in listaPedidos:
            if i[0] %2 == 0:
                self.pedidos.insert("", END, value= i, tag="par")
            else:
                self.pedidos.insert("", END, value= i, tag="impar")
        self.desconectaDb
    def OnDoubleClick(self, event):
        self.limparTela()
        self.pedidos.selection()   
        
        for i in self.pedidos.selection():
            col1, col2, col3, col4, col5 = self.pedidos.item(i, 'values')
            self.enCod.insert(END, col1)
            self.enMesa.insert(END, col2)
            self.strBurg.set(col3)
            self.strBeb.set(col4)
    def deleteComanda(self):
        self.variaveis()
        self.conectaDb()
        self.cursor.execute(""" DELETE FROM pedidos WHERE cod = ? """, (self.cod))
        self.con.commit()
        self.desconectaDb()
        self.limparTela()
        self.selectPedido()
    def updateComanda(self):
        
        self.variaveis()
        self.valor = self.valueBurg + self.valueBeb
        self.conectaDb()
        self.cursor.execute(""" UPDATE pedidos SET mesa = ?, burg = ?, beb = ?, valor = ?
                            WHERE cod = ?""", (self.mesa, self.burg, self.beb, self.valor, self.cod))
        self.con.commit()
        self.desconectaDb()
        self.selectPedido()
        self.limparTela()
    def valueSelector(self, choice):
        self.variaveis()
        valuesBeb = [6.00, 5.50, 5.00]
        valuesBurg = [15.00, 12.00, 10.00, 8.00, 6.00]
        
        if(self.beb == "COCA-COLA") or (self.beb == "PEPSI") or (self.beb == "GUARANA"):
            self.valueBeb = valuesBeb[0] 
        elif(self.beb == "GUARA MIX") or (self.beb == "SPRITE"):
            self.valueBeb = valuesBeb[1]
        elif(self.beb == "FANTA") or (self.beb == "FANTA UVA") or (self.beb == "FANTA GUARANA"):
            self.valueBeb = valuesBeb[2]
        else:
            self.valueBeb = 0
        
        if(self.burg == "X-TUDO"):
            self.valueBurg = valuesBurg[0]
        elif(self.burg == "AMERICANO") or (self.burg == "BACON"):
            self.valueBurg = valuesBurg[1]
        elif(self.burg == "X-BURGUER") or (self.burg == "FRANGO"):
            self.valueBurg = valuesBurg[2]
        elif(self.burg == "X-SALADA"):
            self.valueBurg = valuesBurg[3]
        elif(self.burg == "MISTO"):
            self.valueBurg = valuesBurg[4]
        else:
            self.valueBurg = 0
        print(self.valueBeb)
        print(self.valueBurg)
        
        
        
class Application(Funcs):
    def __init__(self):
        self.win = win
        self.tela()
        self.framesTela()
        self.widgetsF01()
        self.infosPedidos()
        self.criarTabela()
        self.selectPedido()
        win.mainloop()   
    def tela(self):
        self.win.title("Sistema de Pedidos")
        self.win.configure(background="#f4b438")
        self.win.iconbitmap("images/ico.ico")
        self.win.geometry("400x400")
        self.win.resizable(False, False)
    def framesTela(self):
        self.frame01 = Frame(self.win, bg="#202020")
        self.frame01.place(relx= 0, rely= 0 , relwidth= 1, relheight= 0.5) 
        
        self.frame02 = Frame(self.win, bg="#202020")
        self.frame02.place(relx= 0, rely= 0.5, relwidth= 1, relheight= 0.5)             
    def widgetsF01(self):
        
        # BUTTONS #
            # BLOCO 1 #
        self.btnCadastrar = Button(self.frame01, text= "CADASTRAR", bd= 0, bg="#67d36e", fg= "#202020", font=("arial black", 8), highlightthickness=50, command= self.addPedido)
        self.btnCadastrar.place(relx= 0.1, rely= 0.47, relwidth= 0.8, relheight= 0.15)
            
            # BLOCO 2 #
        self.btnAlt = Button(self.frame01, text= "ALTERAR", bd= 0, bg="#f4b438", fg= "#202020", font=("arial black", 8), highlightthickness=50, command= self.updateComanda)
        self.btnAlt.place(relx= 0.1, rely= 0.66, relwidth= 0.25, relheight= 0.15)
        
        self.btnLimpar = Button(self.frame01, text= "LIMPAR", bd= 0, bg="#f4b438", fg= "#202020", font=("arial black", 8), highlightthickness=50, command= self.limparTela)
        self.btnLimpar.place(relx= 0.375, rely= 0.66, relwidth= 0.25, relheight= 0.15)
        
        self.btnApg = Button(self.frame01, text= "APAGAR", bd= 0, bg="#f43838", fg= "#202020", font=("arial black", 8), highlightthickness=50, command= self.deleteComanda)
        self.btnApg.place(relx= 0.65, rely= 0.66, relwidth= 0.25, relheight= 0.15)
        
        # LABELS & ENTRYS #
        self.lbMesa = Label(self.frame01, background= "#202020", font= ("arial", 8, "bold"), text="Mesa", fg="white")
        self.lbMesa.place(relx= 0.05, rely= 0.15)
        self.enMesa = Entry(self.frame01, background= "#888787", bd= 0, fg="#f1f1f1", font=("arial", 8, "bold"), justify= CENTER)
        self.enMesa.place(relx= 0.145, rely= 0.15, relwidth= 0.15, relheight= 0.09)
        
        self.enCod = Entry(self.frame01)
        
        # OPTION MENUS #
        self.strBurg = StringVar(self.frame01)
        self.tipB = ("Misto", "X-Salada", "X-Burguer", "Frango", "Bacon", "Americano", "X-Tudo")
        self.strBurg.set("Hamburguer")
        self.menBurg = OptionMenu(self.frame01, self.strBurg, *self.tipB, command= self.valueSelector)
        self.menBurg.config(bg= "#888787", font=("arial", 8, "bold"), fg= "white", bd= 0, highlightthickness= 0.7, highlightbackground= "#999999")
        self.menBurg.place(relx= 0.31, rely= 0.15, relwidth= 0.535, relheight= 0.09)
        
        self.strBeb = StringVar(self.frame01)
        self.tipBe = ("Coca-Cola", "Pepsi", "Guarana", "Guara Mix", "Sprite", "Fanta", "Fanta Uva", "Fanta Guarana")
        self.strBeb.set("Bebida")
        self.menBeb = OptionMenu(self.frame01, self.strBeb, *self.tipBe, command= self.valueSelector)
        self.menBeb.config(bg= "#888787", font=("arial", 8, "bold"), fg= "white", bd= 0, highlightthickness= 0.7, highlightbackground= "#999999")
        self.menBeb.place(relx= 0.145, rely= 0.270, relwidth= 0.7, relheight= 0.09)       
    def infosPedidos(self):
        self.pedidos = ttk.Treeview(self.frame02, columns= ("Col1", "Col2", "Col3", "Col4", "col5"), height= 3)
        self.pedidos.heading("#0", text= "")
        self.pedidos.heading("#1", text= "O", anchor=CENTER)
        self.pedidos.heading("#2", text= "M", anchor=CENTER)
        self.pedidos.heading("#3", text= "Hamburguer", anchor=CENTER)
        self.pedidos.heading("#4", text= "Bebida", anchor=CENTER)
        self.pedidos.heading("#5", text= "Valor", anchor=CENTER)
        
        self.pedidos.column("#0", width= 0, stretch= NO)
        self.pedidos.column("#1", width= 0, anchor=CENTER, stretch= NO)
        self.pedidos.column("#2", width= 41, anchor=CENTER)
        self.pedidos.column("#3", width= 110, anchor=CENTER)
        self.pedidos.column("#4", width= 100, anchor=CENTER)
        self.pedidos.column("#5", width= 90, anchor=CENTER)
        
        self.pedidos.place(relx= 0.05, rely= 0, relwidth= 0.85, relheight= 0.85)
        
        self.scrPedidos = Scrollbar(self.frame02, orient="vertical")
        self.pedidos.configure(yscroll=self.scrPedidos.set)
        self.scrPedidos.place(relx= 0.9,rely= 0, relwidth= 0.05, relheight= 0.85)
        self.pedidos.bind("<Double-1>", self.OnDoubleClick)
        
        self.pedidos.tag_configure("par", foreground="white", background="#202020")
        self.pedidos.tag_configure("impar", foreground="black", background="white")

Application()    

