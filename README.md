# 🗨️ Guia para Executar o Projeto 

## ✅ Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

- **Python 3.6 ou superior**  
- **pip** (gerenciador de pacotes do Python) 

Verifique se o Python está instalado:

```bash
python --version
```

## 🛠️ Passo 1: Criar e ativar um Ambiente Virtual (ATENÇÃO: USE O CMD!!!)

```bash
python -m venv venv
cd venv
Scripts\activate.bat
```

## 📦 Passo 2: Retorne a raiz do projeto e instale as dependências
```bash
cd ..
pip install grpcio grpcio-tools wheel
```

## 🧾 Passo 3: Gerar os arquivos python a partir do .proto
```bash
python -m grpc_tools.protoc -Iproto \
    --python_out=proto \
    --grpc_python_out=proto \
    proto/chat.proto
```

## 🐍 Passo 5: Executar o Servidor e o Cliente
### Iniciar o servidor:
```bash
python server.py
```
### Iniciar o cliente (em outra janela do terminal):
```bash
python client.py
```