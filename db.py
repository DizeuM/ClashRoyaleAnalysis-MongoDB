from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = ''

def conectar_banco():
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Conexão com o MongoDB estabelecida com sucesso!")
        return client
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return None