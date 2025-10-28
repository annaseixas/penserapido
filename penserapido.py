import customtkinter as ctk
import mysql.connector
from PIL import Image
import random

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  
        database="pense_rapido"
)

def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

def criar_menu(root):
    menu_frame = ctk.CTkFrame(root)
    menu_frame.pack(fill="both", expand= True)
    img = ctk.CTkImage(light_image=Image.open("penserapidopngtransp.png"), size=(650, 400))
    ctk.CTkLabel(menu_frame, text="", image=img).pack(pady=0)
    btn_cadastro = ctk.CTkButton(menu_frame, text="Cadastrar Perguntas", font=("Arial", 22, "bold"), command=lambda: tela_categorias(root), width=300, height=50, fg_color="orange")
    btn_cadastro.pack(pady=10)
    btn_play = ctk.CTkButton(menu_frame, text="Iniciar Quiz", font=("Arial", 22, "bold"), command=lambda: tela_quiz(root), width=300, height=50, fg_color="orange")
    btn_play.pack(pady=10)

def tela_categorias(root):
    clear_screen(root)
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand= True)

    titulo = ctk.CTkLabel(frame, text="Escolha a Categoria para Cadastro", font=("Arial", 28, "bold"))
    titulo.pack(pady=30)

    categorias = ["Banco de Dados", "Programação", "Manutenção de Software", "LGPD", "Geografia"]

    for cat in categorias:
        btn_cat = ctk.CTkButton(frame, text=cat,  font=("Arial", 22, "bold"), command=lambda c=cat: tela_cadastro_pergunta(root, c), width=300, height=50, fg_color="orange")
        btn_cat.pack(pady=10)

    btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", font=("Arial", 16, "bold"), command=lambda: voltar_menu(root), fg_color="orange")
    btn_voltar.pack(pady=20)

def tela_cadastro_pergunta(root, categoria):
    clear_screen(root)
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True)

    titulo = ctk.CTkLabel(frame, text=f"Cadastrar Pergunta - Categoria: {categoria}", font=("Arial", 28, "bold"))
    titulo.pack(pady=30)

    lbl_pergunta = ctk.CTkLabel(frame, text="Pergunta", font=("Arial", 20, "bold"))
    lbl_pergunta.pack(pady=10)
    pergunta_entry = ctk.CTkEntry(frame, placeholder_text="Digite a pergunta", height=40, width=550)
    pergunta_entry.pack(pady=10)

    lbl_resposta = ctk.CTkLabel(frame, text="Resposta Correta: ", font=("Arial", 20, "bold"))
    lbl_resposta.pack(pady=10)
    resposta_entry = ctk.CTkEntry(frame, placeholder_text="Digite a resposta correta", height=40, width=550)
    resposta_entry.pack(pady=10)

    def salvar():
        pergunta= pergunta_entry.get().strip()
        resposta = resposta_entry.get().strip()

        if not pergunta or not resposta:
            aviso= ctk.CTkLabel(frame, text="Preencha a pergunta e a resposta corretamente!", text_color="red", font=("Arial", 12))
            aviso.pack(pady=10)
            return
        
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO perguntas (pergunta, resposta, categoria)"
                "VALUES (%s, %s, %s)",
                (pergunta, resposta, categoria)
            )
            conn.commit()
            conn.close()

            sucesso = ctk.CTkLabel (frame, text="Pergunta cadastrada com sucesso!", text_color="green", font=("Arial", 12))
            sucesso.pack(pady=20)

            pergunta_entry.delete(0, "end")
            resposta_entry.delete(0, "end")

        except mysql.connector.Error as err:
            erro = ctk.CTkLabel(frame, text=f"Erro no banco: {str(err)}", text_color="red", font=("Arial",12))
            erro.pack(pady=10)

    btn_salvar = ctk.CTkButton(frame, text="Cadastrar", font=("Arial", 16, "bold"), command=salvar, width=150, height=40, fg_color="orange")
    btn_salvar.pack(pady=10)

    def continuar():
        for widget in frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and ("sucesso" in str(widget.cget("text")) or "Error" in str(widget.cget("text")) or "Preencha" in str(widget.cget("text"))):
                widget.destroy()
            pergunta_entry.delete(0, "end")
            resposta_entry.delete(0, "end")

    btn_continuar = ctk.CTkButton(frame, text="Continuar Cadastrando", font=("Arial", 16, "bold"), command=continuar, width=200, height=40, fg_color="orange")
    btn_continuar.pack(pady=10)

    btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", font=("Arial", 16, "bold"), command=lambda: voltar_menu(root), width=150, height=40, fg_color="orange")
    btn_voltar.pack(pady=10)

def voltar_menu(root):
    clear_screen(root)
    criar_menu(root)

def tela_quiz(root):
    clear_screen(root)
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand= True)

    titulo = ctk.CTkLabel(frame, text="Escolha a Categoria para o quiz", font=("Arial", 28, "bold"))
    titulo.pack(pady=30)

    categorias = ["Banco de Dados", "Programação", "Manutenção de Software", "LGPD", "Geografia"]

    for cat in categorias:
        btn_cat = ctk.CTkButton(frame, text=cat, font=("Arial", 22, "bold"), command=lambda c=cat: iniciar_quiz(root, c), width=300, height=50, fg_color="orange")
        btn_cat.pack(pady=10)

    btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", font=("Arial", 16, "bold"), command=lambda: voltar_menu(root), fg_color="orange")
    btn_voltar.pack(pady=20)

def iniciar_quiz(root, categoria):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, pergunta, resposta FROM perguntas WHERE categoria = %s", (categoria,))
        perguntas = cursor.fetchall()
        conn.close()

        random.shuffle(perguntas)
        tela_quiz_perguntas(root, categoria, perguntas)

    except mysql.connector.Error as err:
        clear_screen(root)
        frame = ctk.CTkFrame(root)
        frame.pack(fill="both", expand=True)
        erro = ctk.CTkLabel(frame, text=f"Erro ao carregar perguntas: {str(err)}", text_color="red", font=("Arial", 12))
        erro.pack(pady=20)
        btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", font=("Arial", 22, "bold"), command=lambda: voltar_menu(root), width=200, height=50, fg_color="orange")
        btn_voltar.pack(pady=10)

def proxima_pergunta(root, categoria, perguntas_restantes):
    if perguntas_restantes:
        perguntas_restantes.pop(0)
    tela_quiz_perguntas(root, categoria, perguntas_restantes)

def tela_quiz_perguntas(root, categoria, perguntas_restantes):
    clear_screen(root)
    frame = ctk.CTkFrame(root)
    frame.pack(fill="both", expand=True)

    titulo = ctk.CTkLabel(frame, text=f"Quiz - Categoria: {categoria}", font=("Arial", 28, "bold"))
    titulo.pack(pady=20)
    
    if not perguntas_restantes:
        fim_label = ctk.CTkLabel(frame, text="Fim das perguntas", font=("Arial", 28, "bold"), text_color="dark blue")
        fim_label.pack(pady=50)
        btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", font=("Arial", 22, "bold"), command=lambda: voltar_menu(root), width=200, height=50, fg_color="orange")
        btn_voltar.pack(pady=10)
        return

    id_pergunta, pergunta, resposta_correta = perguntas_restantes[0]

    label_pergunta = ctk.CTkLabel(frame, text=pergunta, font=("Arial", 50, "bold"), wraplength=1000)
    label_pergunta.pack(pady=80)

    label_resposta = ctk.CTkLabel(frame, text="", font=("Arial", 22, "bold"), text_color="dark blue", wraplength=1000)
    label_resposta.pack(pady=20)

    def mostrar_resposta(label, resposta):
        label.configure(text=f"Resposta: {resposta}")

    btn_proxima = ctk.CTkButton(frame, text="Proxima Pergunta", font=("Arial", 22, "bold"), command=lambda: proxima_pergunta(root, categoria, perguntas_restantes), width=200, height=50, fg_color="orange")
    btn_proxima.pack(pady=10)

    btn_resposta = ctk.CTkButton(frame, text="Mostrar Resposta", font=("Arial", 22, "bold"), command=lambda: mostrar_resposta(label_resposta, resposta_correta), width=200, height=50, fg_color="orange")
    btn_resposta.pack(pady=10)

    btn_voltar = ctk.CTkButton(frame, text="Voltar ao Menu", font=("Arial", 22, "bold"), command=lambda: voltar_menu(root), width=200, height=50, fg_color="orange")
    btn_voltar.pack(pady=10)

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.geometry("1000x800")
    root.title("Pense Rápido")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    criar_menu(root)
    root.mainloop()
