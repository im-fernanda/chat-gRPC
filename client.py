import grpc
import threading
import time, uuid
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from datetime import datetime

import proto.chat_pb2 as chat_pb2
import proto.chat_pb2_grpc as chat_pb2_grpc

address = "localhost"
port = 50051
class ClienteChat:
    def __init__(self, nome_usuario, exibir_mensagem_callback):
        self.nome_usuario = nome_usuario
        self.exibir_mensagem_callback = exibir_mensagem_callback
        self.canal = grpc.insecure_channel(address + ":" + str(port))
        self.stub = chat_pb2_grpc.ChatServiceStub(self.canal)
        self.fila_envio = []
        self.ativo = True
        self.client_id = str(uuid.uuid4())

    def gerar_mensagens(self):
        while self.ativo:
            if self.fila_envio:
                mensagem = self.fila_envio.pop(0)
                yield mensagem
            else:
                time.sleep(0.1)

    def iniciar_chat(self):
        def receber_mensagens():
            try:
                for resposta in self.stub.Chat(self.gerar_mensagens()):
                    horario = datetime.fromtimestamp(resposta.timestamp).strftime(
                        "%H:%M:%S"
                    )
                    # Verifica se a mensagem é do próprio usuário
                    if resposta.client_id == self.client_id:
                        remetente = resposta.username + " (você)"
                    else:
                        remetente = resposta.username

                    self.exibir_mensagem_callback(
                        f"[{horario}] {remetente}: {resposta.message}"
                    )
            except grpc.RpcError as e:
                self.exibir_mensagem_callback(f"Erro na conexão: {e}")

        threading.Thread(target=receber_mensagens, daemon=True).start()

    def enviar_mensagem(self, texto):
        mensagem = chat_pb2.ChatMessage(
            username=self.nome_usuario,
            message=texto,
            timestamp=int(time.time()),
            client_id=self.client_id
        )
        self.fila_envio.append(mensagem)

    def parar(self):
        self.ativo = False
        self.canal.close()


class InterfaceChat:
    def __init__(self, root):
        root.withdraw()
        self.nome_usuario = simpledialog.askstring(
            "Nome de Usuário", "Digite seu nome de usuário:", parent=root
        )

        if not self.nome_usuario:
            self.root.destroy()
            return

        root.deiconify()
        self.root = root
        self.root.title("Chat com gRPC")

        self.area_chat = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state="disabled", width=50, height=20
        )
        self.area_chat.pack(padx=10, pady=10)

        self.entrada_mensagem = tk.Entry(root, width=40)
        self.entrada_mensagem.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        self.entrada_mensagem.bind("<Return>", self.enviar_mensagem)

        self.botao_enviar = tk.Button(root, text="Enviar", command=self.enviar_mensagem)
        self.botao_enviar.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

    

        self.cliente = ClienteChat(self.nome_usuario, self.exibir_mensagem)
        self.cliente.iniciar_chat()

        self.root.protocol("WM_DELETE_WINDOW", self.fechar)

    def exibir_mensagem(self, mensagem):
        self.area_chat.configure(state="normal")
        self.area_chat.insert(tk.END, mensagem + "\n")
        self.area_chat.configure(state="disabled")
        self.area_chat.yview(tk.END)

    def enviar_mensagem(self, evento=None):
        texto = self.entrada_mensagem.get()
        if texto:
            self.cliente.enviar_mensagem(texto)
            self.entrada_mensagem.delete(0, tk.END)

    def fechar(self):
        self.cliente.parar()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    interface = InterfaceChat(root)
    root.mainloop()
