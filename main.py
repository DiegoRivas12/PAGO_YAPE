from flask import Flask, render_template, request, jsonify
import mercadopago
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Inicializa Mercado Pago con el Access Token de producción
sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

@app.route("/")
def index():
    return render_template("prueba.html")  # Renderiza el HTML

@app.route("/get_public_key", methods=["GET"])
def get_public_key():
    """ Devuelve la clave pública para el frontend """
    return jsonify({"public_key": os.getenv("MP_PUBLIC_KEY")})

@app.route("/procesar_pago", methods=["POST"])
def procesar_pago():
    """ Procesa el pago con el token generado en el frontend """
    data = request.json
    token = data.get("token")

    payment_data = {
        "transaction_amount": 2000,  # Monto en soles
        "token": token["id"],
        "description": "Compra en mi tienda hoy",
        "installments": 1,
        "payment_method_id": "yape",
        "payer": {"email": "cliente@test.com"}
    }

    try:
        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]
        return jsonify(payment)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
