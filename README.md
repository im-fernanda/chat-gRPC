<h1 align="center" style="font-weight: bold;">  💬 Chat gRPC </h1>

Este projeto é uma aplicação de chat em tempo real desenvolvida em Python, utilizando o framework gRPC para comunicação entre cliente e servidor. O objetivo é demonstrar como implementar uma comunicação eficiente e bidirecional entre processos distribuídos, com suporte a múltiplos clientes simultâneos.

---

## 📌 Visão Geral

- **Tecnologias Utilizadas**:
  - Python 3.6 ou superior
  - gRPC com Protocol Buffers
  - Interface gráfica com Tkinter
- **Arquitetura**:
  - Comunicação cliente-servidor baseada em gRPC
  - Transmissão de mensagens em tempo real
  - Suporte a múltiplos clientes conectados simultaneamente

---


## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

- **Python 3.6 ou superior**  
- **pip** (gerenciador de pacotes do Python) 

Verifique as versões instaladas:

```bash
python --version
pip --version
```

## 🚀 Executando o Projeto

## 🛠️ Passo 1: Instalar as dependências

```bash
python -m pip install --upgrade pip
python -m pip install grpcio grpcio-tools wheel tkinter
```


## 🐍 Passo 2: Executar o Servidor e o Cliente
### Iniciar o servidor:
```bash
python server.py
```
### Iniciar o cliente (em outra janela do terminal):
```bash
python client.py
```

Uma interface gráfica será aberta, permitindo que você envie e receba mensagens em tempo real.

# 🗨️ Guia para GERAR o Projeto 

## 🧾 Gerar os arquivos python a partir do .proto
```bash
python -m grpc_tools.protoc -Iproto \
    --python_out=proto \
    --grpc_python_out=proto \
    proto/chat.proto
```


### O que esse comando está fazendo?

| Parte do comando                                | Explicação                                                                                                           |
|-------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| `python -m grpc_tools.protoc`                   | Executa o compilador `protoc` (Protocol Buffers) via o módulo `grpc_tools` em Python.                                |
| `-I .`                                          | Diz ao `protoc` onde procurar os arquivos `.proto`. Aqui, o ponto `.` significa "**procure na pasta atual**".         |
| `--python_out=.`                                | Gera o código Python **relacionado às mensagens definidas** no `.proto` e salva na pasta atual (`.`).                |
| `--grpc_python_out=.`                           | Gera o código Python **relacionado aos serviços gRPC (client/server stubs)** e salva na pasta atual.                 |
| `chat.proto`                                    | O arquivo `.proto` que será processado.                                                                              |
