from datetime import datetime
from db import conectar_banco

# Conecta ao banco de dados e seleciona a coleção de batalhas
client = conectar_banco()
db = client['clash_royale']
batalhas_collection = db['batalhas']

def calcular_derrotas_por_combo(combo_cartas, start_time, end_time):

    # Converte os tempos para strings no formato adequado
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S+00:00')
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S+00:00')

    # Define o pipeline de agregação
    pipeline = [
        {"$match": {
            "battle_time": {"$gte": start_time_str, "$lte": end_time_str},
            "loser.deck": {"$all": combo_cartas}  # Verifica se todas as cartas do combo estão no deck do perdedor
        }},
        {"$count": "total_derrotas"}  # Conta as derrotas
    ]

    result = list(batalhas_collection.aggregate(pipeline))
    
    return result[0]['total_derrotas'] if result else 0

# Exemplo de uso
combo_cartas = [26000001, 26000002, 26000010]  # IDs das cartas no combo
start_time = datetime(2021, 1, 1)
end_time = datetime(2021, 12, 31)

quantidade_derrotas = calcular_derrotas_por_combo(combo_cartas, start_time, end_time)
print(f"Quantidade de derrotas com o combo {combo_cartas}: {quantidade_derrotas}")
