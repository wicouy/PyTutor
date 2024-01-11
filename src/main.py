import os
import json
from openai import OpenAI
import speech_recognition as sr
import keyboard
import threading

# Cargar la clave API de OpenAI y el contexto desde config.json
def cargar_configuracion():
    # Obtener el directorio en el que se encuentra el script actual
    directorio_script = os.path.dirname(os.path.realpath(__file__))

    # Construir la ruta completa al archivo config.json
    ruta_config = os.path.join(directorio_script, 'config.json')

    # Abrir el archivo config.json
    with open(ruta_config, 'r') as file:
        data = json.load(file)
        return data["openai_api_key"], data["contexto_bot"]

api_key, contexto_bot = cargar_configuracion()

# Inicializar el reconocedor
r = sr.Recognizer()

# Variable para controlar si la captura de audio está activa
captura_activa = False

# Función para transcribir el audio
def transcribe_audio(audio):
    try:
        text = r.recognize_google(audio, language="es-ES")
        print("Transcripción: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition no pudo entender el audio")
    except sr.RequestError:
        print("No se pudo solicitar resultados desde el servicio de Google Speech Recognition")

# Función para enviar texto a la API de OpenAI
def consulta_openai(texto, api_key, contexto, temperatura=0.3):
    client = OpenAI(api_key=api_key)
    prompt_personalizado = texto

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0613", #"gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": contexto},
                {"role": "user", "content": prompt_personalizado}
            ],
            temperature=temperatura
        )
        if response.choices:
            respuesta = response.choices[0].message.content
            return respuesta.strip()
        else:
            return "No response"
    except Exception as e:
        print(f"Error al consultar la API de OpenAI: {e}")
        return None

# Función para manejar la captura de audio
def manejar_captura():
    global captura_activa
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while captura_activa:
            try:
                audio = r.listen(source, timeout=1.5, phrase_time_limit=5)
                texto_transcrito = transcribe_audio(audio)
                if texto_transcrito:
                    respuesta = consulta_openai(texto_transcrito, api_key, contexto_bot)
                    print("Respuesta de OpenAI: ", respuesta)
            except sr.WaitTimeoutError:
                continue

# Función para iniciar/detener la captura de audio
def toggle_captura():
    global captura_activa
    captura_activa = not captura_activa
    if captura_activa:
        print("Comenzando la captura de audio...")
        threading.Thread(target=manejar_captura).start()
    else:
        print("Deteniendo la captura de audio...")

# Configurar la captura de audio y la escucha de teclas
print("Presiona 'CTRL' para comenzar/detener la escucha, 'p' para salir.")
keyboard.add_hotkey("ctrl", toggle_captura)
keyboard.wait('p')
