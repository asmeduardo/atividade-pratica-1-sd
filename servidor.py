import socket
import json
import xml.etree.ElementTree as ET
import yaml
import toml

# Inicializar o servidor
soquete_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soquete_servidor.bind(('localhost', 3333))
soquete_servidor.listen(1)
print("Servidor aguardando conexão...")

conexao, endereco = soquete_servidor.accept()
print("Conexão estabelecida!")
print()

while True:
    # Receber e decodificar os dados
    dados_serializados = conexao.recv(4096).decode()

    if not dados_serializados:
        break
    
    # Separar o formato dos dados
    formato, dados = dados_serializados.split(':', 1)

    try:
        # Deserializar os dados no formato correspondente
        if formato == 'csv':
            itens_csv = dados.split(',')
            dados = {
                "Nome": itens_csv[0],
                "CPF": itens_csv[1],
                "idade": int(itens_csv[2]),
                "mensagem": itens_csv[3]
            }
        elif formato == 'json':
            dados = json.loads(dados)
        elif formato == 'xml':
            raiz = ET.fromstring(dados)
            dados = {elem.tag: elem.text for elem in raiz}
        elif formato == 'yaml':
            dados = yaml.safe_load(dados)
        elif formato == 'toml':
            dados = toml.loads(dados)

        # Imprimir os dados
        print(f"Formato: {formato}")
        for chave, valor in dados.items():
            print(f"{chave}: {valor}")
        print()
    except Exception as e:
        print(f"Erro ao processar formato {formato}: {e}")

conexao.close()
