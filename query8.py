# Taxa de Derrotas com Determinadas Cartas no Deck
from datetime import datetime
from db import conectar_banco

# Conecta ao banco de dados e seleciona a coleção de batalhas
client = conectar_banco()
db = client['clash_royale']
batalhas_collection = db['batalhas']

def cartas_associadas_a_derrotas(start_time, end_time, limite=10):
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S%z")
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S%z")

    # Agrupa todas as cartas em decks perdedores e conta a frequência de cada carta
    pipeline = [
        {"$match": {"battle_time": {"$gte": start_time_str, "$lte": end_time_str}}},
        {"$unwind": "$loser.deck"},
        {"$group": {"_id": "$loser.deck", "total_derrotas": {"$sum": 1}}},
        {"$sort": {"total_derrotas": -1}},
        {"$limit": limite}
    ]
    
    resultado = list(batalhas_collection.aggregate(pipeline))
    
    return resultado

# Exibe as cartas mais associadas a derrotas
start_time = datetime(2020, 1, 1)
end_time = datetime(2022, 12, 31)
limite = 10  # Define o número máximo de cartas a listar
cartas_derrotas = cartas_associadas_a_derrotas(start_time, end_time, limite)

print("Cartas mais associadas a derrotas:")
for carta in cartas_derrotas:
    print(f"Carta ID {carta['_id']}: {carta['total_derrotas']} derrotas")
