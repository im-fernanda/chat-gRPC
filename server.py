import grpc
from concurrent import futures
import time
import threading

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

clientes = []
historico_mensagens = []

class ServicoChat(rpc.ChatServiceServicer):

    def Chat(self, request_iterator, context):
        """
        Esta é uma chamada do tipo de fluxo de resposta. Isso significa que o servidor pode continuar enviando mensagens
        Todo cliente abre essa conexão e espera o servidor enviar novas mensagens
        """
        fila_cliente = []
        clientes.append(fila_cliente)

        # Envia o histórico para o cliente assim que ele se conectar
        for mensagem in historico_mensagens:
            fila_cliente.append(mensagem)

        def enviar_mensagens():
            try:
                for mensagem in request_iterator:
                    historico_mensagens.append(mensagem)
                    for fila in clientes:
                        fila.append(mensagem)
                    print("[{}] {}".format(mensagem.username, mensagem.message, mensagem.client_id))
            except grpc.RpcError as e:
                print("Cliente desconectado: {}".format(e))
                clientes.remove(fila_cliente)

        threading.Thread(target=enviar_mensagens, daemon=True).start()

        # Para cada cliente, um loop infinito é iniciado (no próprio thread gerenciado do gRPC)
        while True:
            if fila_cliente:
                yield fila_cliente.pop(0)
            time.sleep(0.1)


def iniciar_servidor():
    # Workers é a quantidade de threads que podem ser abertos ao mesmo tempo.
    # Se tiver 10 clientes conectados, então mais clientes não são capazes de se conectar ao servidor.
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Cria um servidor gRPC
    rpc.add_ChatServiceServicer_to_server(
        ServicoChat(), servidor
    )  # registra a classe que implementa o serviço gRPC (no caso, ServidorChat) no servidor.
    servidor.add_insecure_port("[::]:50051")
    servidor.start()  # começa a escutar as requisições
    print("Servidor rodando em :50051")
    servidor.wait_for_termination()


if __name__ == "__main__":
    iniciar_servidor()
