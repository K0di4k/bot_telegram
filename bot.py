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
PORT = int(os.environ.get('PORT', 8080))  # Obtener el puerto de la variable de entorno

# ----------------------------------------------------------------------------
# Función para enviar el mensaje de respuesta a Telegram
# ----------------------------------------------------------------------------

def send_message(chat_id, response_text):
    url = TELEGRAM_API_URL + 'sendMessage'
    data = {'chat_id': chat_id, 'text': response_text}
    requests.post(url, data=data)

# ----------------------------------------------------------------------------
# Clase para manejar las peticiones HTTP entrantes (webhook de Telegram)
# ----------------------------------------------------------------------------

class TelegramWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            update = json.loads(post_data.decode('utf-8'))
            self.process_update(update)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

        self._send_response(200, 'OK')

    def process_update(self, update):
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            message_text = update['message']['text']

            if message_text == '/start':
                response = 'Me has iniciado desde Python en Render!'
            elif message_text == 'info':
                response = 'Información del bot Python en Render...'
            elif message_text == 'Hola!':
                response = '¡Hola a ti también desde Render!'
            elif message_text == 'que haces?':
                response = 'Estoy corriendo en Render y listo para automatizar!'
            elif message_text == 'como crees que te ira en la sumativa:':
                response = 'Con Python y en Render, ¡seguro que super bien!'
            else:
                response = 'No te he entendido (Python en Render)'

            send_message(chat_id, response)

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
