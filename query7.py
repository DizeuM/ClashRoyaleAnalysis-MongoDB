# Identificar Jogadores com Alta Frequência de Uso de Uma Carta Específica
from datetime import datetime
from db import conectar_banco

# Conecta ao banco de dados e seleciona a coleção de batalhas
client = conectar_banco()
db = client['clash_royale']
batalhas_collection = db['batalhas']

def jogadores_com_frequencia_carta(carta_id, start_time, end_time, porcentagem_minima=50):
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S%z")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S%z")

    # Agrupa as batalhas por jogador e calcula o percentual de uso da carta
    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time_str, "$lte": end_time_str}}},
        {"$group": {
            "_id": "$winner.nickname",
            "total_batalhas": {"$sum": 1},
            "usou_carta": {"$sum": {"$cond": [{"$in": [carta_id, "$winner.deck"]}, 1, 0]}}
        }},
        {"$project": {
            "nickname": "$_id",
            "percentual_uso": {"$multiply": [{"$divide": ["$usou_carta", "$total_batalhas"]}, 100]}
        }},
        {"$match": {"percentual_uso": {"$gte": porcentagem_minima}}},
        {"$sort": {"percentual_uso": -1}}
    ]

    resultado = list(batalhas_collection.aggregate(pipeline))
    
    return resultado

# Exibe os jogadores que usam a carta especificada em mais de 50% das batalhas
carta_id = 26000000  # ID da carta
porcentagem_minima = 50  # Percentual mínimo de uso
start_time = datetime(2021, 1, 1)
end_time = datetime(2021, 12, 31)

jogadores = jogadores_com_frequencia_carta(carta_id, start_time, end_time, porcentagem_minima)
print(f"Jogadores que usaram a carta {carta_id} em mais de {porcentagem_minima}% das batalhas:")
for jogador in jogadores:
    print(f"Nickname: {jogador['nickname']}, Percentual de uso: {jogador['percentual_uso']:.2f}%")
