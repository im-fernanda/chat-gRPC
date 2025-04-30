import grpc
from concurrent import futures
import time
import threading

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

clients = []


class ChatService(rpc.ChatServiceServicer):

    def Chat(self, request_iterator, context):
        """
        Esta é uma chamada do tipo de fluxo de resposta. Isso significa que o servidor pode continuar enviando mensagens
        Todo cliente abre essa conexão e espera o servidor enviar novas mensagens
        """
        client_queue = []
        clients.append(client_queue)

        def send_messages():
            for message in request_iterator:
                for queue in clients:
                    queue.append(message)
            print("[{}] {}".format(message.name, message.message))
        threading.Thread(target=send_messages).start()

        # Para cada cliente, um loop infinito é iniciado (no próprio thread gerenciado do gRPC)
        while True:
            if client_queue:
                yield client_queue.pop(0)
            time.sleep(0.1)


def start_server():
    # Workers é a quantidade de threads que podem ser abertos ao mesmo tempo.
    # Se tiver 10 clientes conectados, então mais clientes não são capazes de se conectar ao servidor.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # Cria um servidor gRPC
    rpc.add_ChatServiceServicer_to_server(
        ChatService(), server
    )  # registra a classe que implementa o serviço gRPC (no caso, ChatService) no servidor.
    server.add_insecure_port("[::]:50051")
    server.start()  # começa a escutar as requisições
    print("Servidor rodando em :50051")
    server.wait_for_termination()


if __name__ == "__main__":
    start_server()
