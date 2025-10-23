import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# --- Información del sistema ---
st.write("Versión de Python:", platform.python_version())

# --- Variables iniciales ---
velocidad = 0.0
motor = "APAGADO"
estado_auto = "🅿️ El auto está detenido"

# --- Funciones MQTT ---
def on_publish(client, userdata, result):
    print("Dato publicado correctamente\n")

def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.write("📩 Mensaje recibido:", message_received)

# --- Configuración del broker ---
broker = "broker.mqttdashboard.com"
port = 1883
client = paho.Client("CAR_SPEED_DAVID")
client.on_message = on_message

# --- Interfaz principal ---
st.title("🏎️ Control y Monitoreo de Velocidad — MQTT")

# --- Control del motor ---
col1, col2 = st.columns(2)

with col1:
    if st.button('Encender Motor 🔑'):
        motor = "ENCENDIDO"
        estado_auto = "🚗 El auto está listo para arrancar"
        client.connect(broker, port)
        mensaje = json.dumps({"Motor": motor})
        client.publish("auto/motor", mensaje)
        st.success("Motor encendido")

with col2:
    if st.button('Apagar Motor 📴'):
        motor = "APAGADO"
        estado_auto = "🅿️ El auto está apagado"
        client.connect(broker, port)
        mensaje = json.dumps({"Motor": motor})
        client.publish("auto/motor", mensaje)
        st.warning("Motor apagado")

st.write("---")

# --- Velocidad y potencia ---
velocidad = st.slider('Velocidad del vehículo (km/h)', 0.0, 200.0, 0.0)
potencia = round((velocidad / 200) * 100, 1)

if motor == "ENCENDIDO":
    if velocidad > 0:
        estado_auto = f"🏁 El auto va a {velocidad} km/h"
    else:
        estado_auto = "🚦 El auto está encendido pero detenido"

# --- Enviar datos ---
if st.button('Enviar Velocidad 📤'):
    client.connect(broker, port)
    mensaje = json.dumps({"Velocidad": velocidad, "Potencia (%)": potencia})
    client.publish("auto/velocidad", mensaje)
    st.info(f"Velocidad enviada: {velocidad} km/h")
    st.progress(int(potencia))

# --- Estado actual ---
st.write("---")
st.subheader("📊 Estado del vehículo")
st.write(estado_auto)
st.metric(label="Potencia del motor", value=f"{potencia} %")


