import json
import requests
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# ----------------------------------------------------------------------------
# Configuración básica
# ----------------------------------------------------------------------------

TOKEN = os.environ.get('BOT_TOKEN')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'
PORT = int(os.environ.get('PORT', 8080))

# ----------------------------------------------------------------------------
# Función para enviar el mensaje de respuesta a Telegram
# ----------------------------------------------------------------------------

def send_message(chat_id, text, reply_markup=None):
    url = TELEGRAM_API_URL + 'sendMessage'
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'} # Usar Markdown por defecto
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    try:
        response = requests.post(url, data=data)
        response.raise_for_status() # Levanta una excepción para códigos de error HTTP
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

# ----------------------------------------------------------------------------
# Clase para manejar las peticiones HTTP entrantes (webhook de Telegram)
# ----------------------------------------------------------------------------

class TelegramWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            update = json.loads(post_data)
            self.process_update(update)
            self._send_response(200, 'OK')
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e} - Data: {post_data}")
            self._send_response(400, 'Bad Request: Invalid JSON')
        except Exception as e:
            print(f"Error processing update: {e} - Update: {update}")
            self._send_response(500, 'Internal Server Error')

    def process_update(self, update):
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            if 'text' in message:
                text = message['text']

                if text == '/start':
                    keyboard = {
                        'keyboard': [['info'], ['Hola!', 'que haces?'], ['como crees que te ira en la sumativa:']],
                        'resize_keyboard': True,
                        'one_time_keyboard': True
                    }
                    send_message(chat_id, '¡Me has iniciado desde Python en Render!', reply_markup=keyboard)
                elif text == 'info':
                    send_message(chat_id, '*Información del bot Python en Render*\nEste es un bot de prueba.')
                elif text == 'Hola!':
                    send_message(chat_id, '¡Hola a ti también desde Render!')
                elif text == 'que haces?':
                    send_message(chat_id, '_Estoy corriendo en Render y listo para automatizar!_')
                elif text == 'como crees que te ira en la sumativa:':
                    send_message(chat_id, 'Con *Python* y en `Render`, ¡seguro que super bien!')
                else:
                    send_message(chat_id, 'No te he entendido (Python en Render)')

# ----------------------------------------------------------------------------
# Función para manejar errores de respuesta
# ----------------------------------------------------------------------------

    def _send_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

# ----------------------------------------------------------------------------
# Iniciar el servidor web
# ----------------------------------------------------------------------------

def main():
    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, TelegramWebhookHandler)
    print(f"Webhook server listening on port {PORT}...")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
