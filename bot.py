import json
import requests
import os

# ----------------------------------------------------------------------------
# Configuración básica
# ----------------------------------------------------------------------------

TOKEN = os.environ.get('BOT_TOKEN')  # Obtener el token de una variable de entorno
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'

# ----------------------------------------------------------------------------
# Función para enviar el mensaje de respuesta a Telegram
# ----------------------------------------------------------------------------

def send_message(chat_id, response_text):
    url = TELEGRAM_API_URL + 'sendMessage'
    data = {'chat_id': chat_id, 'text': response_text}
    requests.post(url, data=data)

# ----------------------------------------------------------------------------
# Manejar las actualizaciones del webhook
# ----------------------------------------------------------------------------

def main():
    try:
        request_body_str = os.environ.get('REQUEST_BODY')
        if request_body_str:
            update = json.loads(request_body_str)

            if 'message' in update:
                chat_id = update['message']['chat']['id']
                message_text = update['message']['text']

                # ------------------------------------------------------------------------
                # Lógica de respuesta basada en el mensaje recibido
                # ------------------------------------------------------------------------

                if message_text == '/start':
                    response = 'Me has iniciado'
                elif message_text == 'info':
                    response = 'Información del bot... (aquí podrías agregar más)'
                elif message_text == 'Hola!':
                    response = '¡Hola!'
                elif message_text == 'que haces?':
                    response = 'aqui estudiando la semana 2 de automatizacion'
                elif message_text == 'como crees que te ira en la sumativa:':
                    response = 'super bien, hice los ejercicios y vi los videos'
                else:
                    response = 'No te he entendido'

                # ------------------------------------------------------------------------
                # Enviar la respuesta
                # ------------------------------------------------------------------------

                send_message(chat_id, response)
    except Exception as e:
        print(f"Error processing update: {e}")

if __name__ == "__main__":
    main()