import socket
import hashlib

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # abre o socket
servidor.bind(('127.0.0.1', 5000)) # seleciona o ip e porta
servidor.listen() # inicia estado de espera ou "listening"

sha256 = hashlib.sha256() # cria o objeto sha256

print("Servidor aguardando conexão...")

conexao, endereco = servidor.accept() # aceitar a conexao com o clinete
print("Conectado por", endereco)

# recebe o nome do arquivo
nomeArquivo = b'' 
while not nomeArquivo.endswith(b'\n'):
    nomeArquivo += conexao.recv(1)
nomeArquivo = nomeArquivo.strip().decode() 

# recebe o hash do arquivo
hashArquivo = b''
while not hashArquivo.endswith(b'\n'):
    hashArquivo += conexao.recv(1)
hashArquivo = hashArquivo.strip().decode()

# recebe o arquivo e o hash 
with open(nomeArquivo, "wb") as f:
    dados = conexao.recv(8192)
    f.write(dados) # salva o arquivo no diretorio "servidor"
    sha256.update(dados) # calcula o hash do arquivo recebido

hashCalculado = sha256.hexdigest()

if hashCalculado == hashArquivo:
    conexao.sendall(b'Hash coincide - Arquivo Integro\n ') # envia resposta para o cliente do sucesso
else:
    conexao.sendall(b'Hash nao coincide - Arquivo Corrompido\n') # envia resposta para o cliente do erro

conexao.close() # fecha a conexao