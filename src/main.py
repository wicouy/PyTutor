import speech_recognition as sr
import keyboard

# Inicializar el reconocedor
r = sr.Recognizer()

# Variable para almacenar el texto transcrito
transcribed_text = ""

# Función para transcribir el audio
def transcribe_audio(audio):
    global transcribed_text
    try:
        # Uso de reconocimiento de Google
        text = r.recognize_google(audio, language="es-ES")
        transcribed_text += text + " "
        print("Transcripción: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition no pudo entender el audio")
    except sr.RequestError:
        print("No se pudo solicitar resultados desde el servicio de Google Speech Recognition")

# Captura de audio
with sr.Microphone() as source:
    print("Mantén presionado 'CTRL' para transcribir y presiona 'p' para cerrar la aplicación.")
    while True:
        if keyboard.is_pressed('ctrl'):
            print("Transcribiendo...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            transcribe_audio(audio)
        elif keyboard.is_pressed('p'):  # Presiona 'p' para cerrar la aplicación
            print("Cerrando la aplicación.")
            break
