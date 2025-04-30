import grpc
import threading
import time
from datetime import datetime

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc


def get_current_timestamp():
    return int(datetime.now().timestamp())


class Client:
    def __init__(self, username):
        self.username = username
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = rpc.ChatServiceStub(self.channel)
        self.stop_event = threading.Event()

    def message_generator(self):
        while not self.stop_event.is_set():
            try:
                message = input()
                if message.lower() == "/sair":
                    self.stop_event.set()
                    break

                yield chat.ChatMessage(
                    username=self.username,
                    message=message,
                    timestamp=get_current_timestamp(),
                )
            except KeyboardInterrupt:
                self.stop_event.set()
                break

    def listen_for_messages(self):
        responses = self.stub.Chat(self.message_generator())

        try:
            for response in responses:
                if response.username != self.username:
                    print(f"\n[{response.username}] {response.message}")
        except grpc.RpcError as e:
            print("Conexão encerrada.")
        finally:
            self.stop_event.set()

    def start(self):
        print(
            f"{self.username} entrou no chat. Digite mensagens ou '/sair' para sair.\n"
        )

        # Thread para escutar mensagens do servidor
        listen_thread = threading.Thread(target=self.listen_for_messages)
        listen_thread.start()

        # Espera o encerramento da thread principal (input)
        while not self.stop_event.is_set():
            time.sleep(0.1)

        print("Saindo do chat...")
        self.channel.close()


if __name__ == "__main__":
    nome = input("Digite seu nome de usuário: ")
    client = Client(nome)
    client.start()
