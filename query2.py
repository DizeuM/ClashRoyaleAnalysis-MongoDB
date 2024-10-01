from datetime import datetime
from db import conectar_banco

# Conecta ao banco de dados e seleciona a coleção de batalhas
client = conectar_banco()
db = client['clash_royale']
batalhas_collection = db['batalhas']

def criar_pipeline(min_porcentagem, min_vitorias, start_time_str, end_time_str):

    return [
        {"$match": {"battle_time": {"$gte": start_time_str, "$lte": end_time_str}}},
        {"$group": {
            "_id": "$winner.deck",
            "total_vitorias": {"$sum": 1}
        }},
        {"$match": {"total_vitorias": {"$gte": min_vitorias}}},  # Filtra decks com vitórias mínimas
        {"$project": {
            "_id": 1,
            "total_vitorias": 1,
            "porcentagem_vitorias": {
                "$multiply": [
                    {"$divide": ["$total_vitorias", {"$sum": "$total_vitorias"}]},  # Calcula a porcentagem
                    100
                ]
            }
        }},
        {"$match": {"porcentagem_vitorias": {"$gte": min_porcentagem}}}  # Filtra por porcentagem mínima
    ]

def listar_decks_com_vitorias(min_porcentagem, min_vitorias, start_time, end_time):
    
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S+00:00')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S+00:00')
    
    pipeline = criar_pipeline(min_porcentagem, min_vitorias, start_time_str, end_time_str)

    # Executa a agregação no MongoDB e retorna os resultados
    return list(batalhas_collection.aggregate(pipeline, allowDiskUse=True))


min_vitorias = 600
min_porcentagem = 90.0
start_time = datetime(2021, 1, 1)
end_time = datetime(2021, 12, 31)

decks = listar_decks_com_vitorias(min_porcentagem, min_vitorias, start_time, end_time)
print(f"Decks com mais de {min_porcentagem}% de vitórias: {decks}")
