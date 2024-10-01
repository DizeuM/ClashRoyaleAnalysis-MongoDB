from datetime import datetime, timedelta
from db import conectar_banco

# Conecta ao banco de dados e seleciona a coleção de batalhas
client = conectar_banco()
db = client['clash_royale']
batalhas_collection = db['batalhas']

def calcular_vitorias_com_carta(com_id, porcentagem, start_time, end_time):
    # Converte os tempos para strings no formato adequado
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S+00:00')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S+00:00')

    # Define o pipeline de agregação
    pipeline = [
        {"$match": {
            "battle_time": {"$gte": start_time_str, "$lte": end_time_str},
            "winner.deck": com_id,
            "loser.crowns": {"$gte": 2}  # O perdedor deve ter derrubado pelo menos 2 torres
        }},
        {"$project": {
            "vencedor_trofes": "$winner.startingTrophies",
            "perdedor_trofes": "$loser.startingTrophies",
            "vitoria": "$winner.tag"
        }},
        {"$match": {
            "$expr": {
                "$lt": [
                    {"$divide": [
                        {"$subtract": ["$perdedor_trofes", "$vencedor_trofes"]}, 
                        "$perdedor_trofes"
                    ]},
                    porcentagem / 100.0  # Compara a diferença percentual
                ]
            }
        }},
        {"$count": "total_vitorias"}  # Conta as vitórias que atendem aos critérios
    ]

    result = list(batalhas_collection.aggregate(pipeline))
    
    # Retorna o número de vitórias, ou 0 se não houver resultados
    return result[0]['total_vitorias'] if result else 0


com_id = 26000000  # ID da carta
porcentagem = 20  # Porcentagem de diferença de troféus
start_time = datetime(2021, 1, 1)
end_time = datetime(2021, 12, 31)

quantidade_vitorias = calcular_vitorias_com_carta(com_id, porcentagem, start_time, end_time)
print(f"Quantidade de vitórias com a carta {com_id}: {quantidade_vitorias}")
