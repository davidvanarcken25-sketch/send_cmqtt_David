import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Información del sistema
st.write("Versión de Python:", platform.python_version())

# Variables iniciales
velocidad = 0.0
motor = "APAGADO"

# Funciones MQTT
def on_publish(client, userdata, result):
    print("Dato publicado con éxito\n")
    pass

def on_message(client, userdata, message):
    global message_received
    message_received = str(message.payload.decode("utf-8"))
    st.write("Mensaje recibido:", message_received)

# Configuración del broker
broker = "broker.mqttdashboard.com"
port = 1883
client = paho.Client("CAR_CONTROL_DAVID")
client.on_message = on_message

# Interfaz principal
st.title("🚗 Control de Velocidad del Auto — MQTT")

# Botón para encender el motor
if st.button('Encender motor'):
    motor = "ENCENDIDO"
    client = paho.Client("CAR_CONTROL_DAVID")
    client.on_publish = on_publish
    client.connect(broker, port)
    mensaje = json.dumps({"Motor": motor})
    client.publish("auto/motor", mensaje)
    st.success("Motor encendido 🚘")

# Botón para apagar el motor
if st.button('Apagar motor'):
    motor = "APAGADO"
    client = paho.Client("CAR_CONTROL_DAVID")
    client.on_publish = on_publish
    client.connect(broker, port)
    mensaje = json.dumps({"Motor": motor})
    client.publish("auto/motor", mensaje)
    st.warning("Motor apagado 💤")

# Control de velocidad
velocidad = st.slider('Selecciona la velocidad del auto (km/h)', 0.0, 200.0, 0.0)
st.write(f"Velocidad seleccionada: {velocidad} km/h")

if st.button('Enviar velocidad'):
    client = paho.Client("CAR_CONTROL_DAVID")
    client.on_publish = on_publish
    client.connect(broker, port)
    mensaje = json.dumps({"Velocidad": float(velocidad)})
    client.publish("auto/velocidad", mensaje)
    st.info(f"Velocidad enviada: {velocidad} km/h 🚀")


