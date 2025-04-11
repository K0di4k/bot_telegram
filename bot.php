<?php

// ----------------------------------------------------------------------------
// Configuración básica
// ----------------------------------------------------------------------------

$token = 'TU_TOKEN_VA_AQUI'; // Reemplaza con el token real de tu bot
$website = 'https://api.telegram.org/bot' . $token;

// ----------------------------------------------------------------------------
// Obtener y decodificar la información del webhook
// ----------------------------------------------------------------------------

$input = file_get_contents('php://input');
$update = json_decode($input, TRUE);

// ----------------------------------------------------------------------------
// Extraer información relevante del mensaje (si existe)
// ----------------------------------------------------------------------------

if (isset($update['message'])) {
    $chatId = $update['message']['chat']['id'];
    $message = $update['message']['text'];

    // ------------------------------------------------------------------------
    // Lógica de respuesta basada en el mensaje recibido
    // ------------------------------------------------------------------------

    switch ($message) {
        case '/start':
            $response = 'Me has iniciado';
            break;

        case 'info':
            $response = 'Información del bot... (aquí podrías agregar más)';
            break;

        case 'Hola!':
            $response = '¡Hola!';
            break;

        case 'que haces?':
            $response = 'aqui estudiando la semana 2 de automatizacion';
            break;

        case 'como crees que te ira en la sumativa:':
            $response = 'super bien, hice los ejercicios y vi los videos';
            break;

        default:
            $response = 'No te he entendido';
            break;
    }

    // ------------------------------------------------------------------------
    // Función para enviar el mensaje de respuesta a Telegram
    // ------------------------------------------------------------------------

    function sendMessage($chat_id, $response_text) {
        global $website;
        $url = $website . '/sendMessage?chat_id=' . $chat_id . '&text=' . urlencode($response_text);
        file_get_contents($url);
    }

    // ------------------------------------------------------------------------
    // Enviar la respuesta
    // ------------------------------------------------------------------------

    sendMessage($chatId, $response);
}

?>
