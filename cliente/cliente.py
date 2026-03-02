import sys
import socket
import os
import hashlib

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # abre o socket
sha256 = hashlib.sha256() # cria o objeto sha256

ip = sys.argv[1] # endereco de ip
porta = 5000 # porta
arquivo = sys.argv[2] # arquivo do argumento
nomeArquivo = os.path.basename(arquivo) # recebe o nome do arquivo

cliente.connect((ip, porta)) # conecta com o servidor

# primeiro calcula o hash do arquivo selecionado
with open(arquivo, 'rb') as f: 
    while True:
        dados = f.read(4096)
        if not dados:
            break
        sha256.update(dados)

hashArquivo = sha256.hexdigest() 

cliente.sendall(nomeArquivo.encode() + b'\n') # envia o nome do arquivo
cliente.sendall(hashArquivo.encode() + b'\n') # envia o hash do arquivo

# abre o arquivo para enviar
with open(arquivo, 'rb') as f:
    while True:
        dados = f.read(4096)
        if not dados:
            break
        cliente.sendall(dados)

cliente.shutdown(socket.SHUT_WR) # avisa quando terminar de enviar os dados

# recebe a resposta do servidor
resposta = cliente.recv(1024)
print(resposta)

# fecha o cliente
cliente.close()