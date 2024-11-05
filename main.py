import os

from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

app = Flask(__name__)

# Reemplaza por tu cadena de conexión de MongoDB Atlas
client = MongoClient(os.getenv("mongo_url"))
db = client["pruebas"]
collection = db["nombre-vuelta"]


# Endpoint para obtener la lista de jugadores ordenada de forma descendente por "vueltas"
@app.route('/obtener', methods=['GET'])
def get_jugadores():
    jugadores = list(collection.find().sort("vueltas", -1))
    for jugador in jugadores:
        jugador["_id"] = str(jugador["_id"])  # Convertir ObjectId a string
    return jsonify(jugadores)

# Endpoint para agregar un nuevo jugador
@app.route('/jugadores', methods=['POST'])
def add_jugador():
    data = request.json
    nombre = data.get('nombre')
    vueltas = data.get('vueltas')

    if nombre and vueltas:
        jugador_id = collection.insert_one({
            "nombre": nombre,
            "vueltas": int(vueltas)
        }).inserted_id
        return jsonify({"msg": "Jugador añadido", "id": str(jugador_id)}), 201
    else:
        return jsonify({"error": "Faltan datos"}), 400

if __name__ == '__main__':
    app.run(debug=True,port=5001)
