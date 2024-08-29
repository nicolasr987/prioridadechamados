import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

chamados = []

@app.route('/api/chamado', methods=['POST'])
def criar_chamado():
    sistema = request.form['sistema']
    descricao = request.form['descricao']
    evidencia = request.files.get('evidencia')

    evidencia_path = None
    if evidencia:
        evidencia_path = os.path.join(UPLOAD_FOLDER, evidencia.filename)
        evidencia.save(evidencia_path)

    chamado = {
        'sistema': sistema,
        'descricao': descricao,
        'evidencia': evidencia_path if evidencia else None
    }

    chamados.append(chamado)

    return jsonify({'status': 'success', 'message': 'Chamado recebido com sucesso!'})

@app.route('/api/chamados', methods=['GET'])
def listar_chamados():
    return jsonify(chamados)

def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False)

# Iniciando o Flask em uma nova thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Interface gráfica Tkinter
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

def atualizar_chamados():
    try:
        response = requests.get('http://127.0.0.1:5000/api/chamados')
        if response.status_code == 200:
            chamados = response.json()
            lista_chamados.delete(1.0, tk.END)  # Limpa a lista atual
            for chamado in chamados:
                lista_chamados.insert(tk.END, f"Sistema: {chamado['sistema']}\nDescrição: {chamado['descricao']}\n")
                
                if chamado['evidencia']:
                    img_path = chamado['evidencia']
                    try:
                        img = Image.open(img_path)
                        img.thumbnail((200, 200))  # Redimensiona a imagem
                        img_tk = ImageTk.PhotoImage(img)
                        lista_chamados.image_create(tk.END, image=img_tk)
                        lista_chamados.insert(tk.END, '\n\n')
                        lista_chamados.image = img_tk
                    except Exception as e:
                        lista_chamados.insert(tk.END, f"Não foi possível carregar a imagem: {e}\n\n")
        else:
            messagebox.showerror("Erro", "Não foi possível carregar os chamados.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao se conectar com o servidor: {e}")

# Criação da janela principal
root = tk.Tk()
root.title("Visualizar Chamados")

# Lista de Chamados
tk.Label(root, text="Chamados Recebidos:").pack()
lista_chamados = tk.Text(root, height=20, width=80)
lista_chamados.pack()

# Botão para atualizar Chamados
tk.Button(root, text="Atualizar Chamados", command=atualizar_chamados).pack()

# Inicializa a interface com a lista de chamados
atualizar_chamados()

# Loop principal do Tkinter
root.mainloop()
