from datetime import datetime
from db import conectar_banco

# Conecta ao banco de dados e seleciona a coleção de batalhas
client = conectar_banco()
db = client['clash_royale']
batalhas_collection = db['batalhas']

def calcular_vitorias_por_carta(carta_id, start_time, end_time):
    # Converte os objetos datetime para strings no formato adequado para a consulta
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S%z")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S%z")

    # Conta o total de batalhas no intervalo de tempo especificado
    total_batalhas = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str}
    })
    
    # Conta o número de vitórias com a carta especificada no mesmo intervalo
    vitorias_com_carta = batalhas_collection.count_documents({
        "battle_time": {"$gte": start_time_str, "$lte": end_time_str},
        "winner.deck": carta_id
    })

    # Retorna a porcentagem de vitórias, evitando divisão por zero
    return (vitorias_com_carta / total_batalhas * 100) if total_batalhas > 0 else 0

# Definindo o ID da carta e o intervalo de datas para a análise
carta_id = 26000000
start_time = datetime(2020, 1, 1)
end_time = datetime(2022, 12, 31)

# Exibe a porcentagem de vitórias com a carta especificada
print(f"Porcentagem de vitórias com a carta {carta_id}: {calcular_vitorias_por_carta(carta_id, start_time, end_time):.2f}%")
