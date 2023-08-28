import socket
import json
import xml.etree.ElementTree as ET
import yaml
import toml
import time

# Formatos de serialização
formatos = ['csv', 'json', 'xml', 'yaml', 'toml']

while True:
    # Coletar dados da mensagem do usuário
    nome = input("Digite o nome: ")
    cpf = input("Digite o CPF: ")
    idade = int(input("Digite a idade: "))
    mensagem = input("Digite a mensagem: ")

    dados = {
        "Nome": nome,
        "CPF": cpf,
        "idade": idade,
        "mensagem": mensagem
    }

    # Conectar ao servidor
    cliente_soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_soquete.connect(('localhost', 3333))

    for formato in formatos:
        # Serializar os dados no formato correspondente
        if formato == 'csv':
            dados_serializados = f"csv:{nome},{cpf},{idade},{mensagem}"
        elif formato == 'json':
            dados_serializados = f"json:{json.dumps(dados)}"
        elif formato == 'xml':
            raiz = ET.Element("mensagem")
            for chave, valor in dados.items():
                ET.SubElement(raiz, chave).text = str(valor)
            dados_serializados = f"xml:{ET.tostring(raiz, encoding='utf-8').decode('utf-8')}"
        elif formato == 'yaml':
            dados_serializados = f"yaml:{yaml.dump(dados)}"
        elif formato == 'toml':
            dados_serializados = f"toml:{toml.dumps(dados)}"

        # Mostrar os dados no console antes de enviar
        print(f"Dados serializados ({formato}):\n{dados_serializados}\n")
        
        # Enviar os dados serializados
        cliente_soquete.send(dados_serializados.encode())

        time.sleep(4)  # Aguardar 4 segundos antes de enviar novamente
    
    cliente_soquete.close()
