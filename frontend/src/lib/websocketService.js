import { ref } from 'vue';

let ws;
let reconnectAttempts = 0;
let heartbeatInterval;

// Create a reactive ref to store the received message
const receivedMessage = ref(null);

const initializeWebSocket = () => {
    ws = new WebSocket('ws://'+ import.meta.env.VITE_SERVER_URL +'/ws/client');

    ws.onopen = () => {
        console.log('WebSocket Connected');
        reconnectAttempts = 0;
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        // console.log('Received message:', data);
        receivedMessage.value = data;
    };

    ws.onclose = () => {
        console.log('WebSocket Disconnected');
        clearInterval(heartbeatInterval);
        attemptReconnect();
    };

    ws.onerror = (error) => {
        console.log('WebSocket Error:', error);
        clearInterval(heartbeatInterval);
        ws.close(); // Ensure it's closed before attempting reconnection
    };
};

const sendMessage = (action, message, recipient = "server") => {
    if (ws?.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            "from": "client",
            "to": recipient,
            "action": action,
            "message": message
        }));
    } else {
        console.warn('WebSocket not open. Message not sent:', message);
    }
};



const attemptReconnect = () => {
    if (reconnectAttempts < 5) {
        setTimeout(() => {
            console.log(`Attempting to reconnect... (${reconnectAttempts + 1})`);
            reconnectAttempts++;
            initializeWebSocket();
        }, 2000 * reconnectAttempts); // Backoff delay (e.g., 2s, 4s, 6s, etc.)
    } else {
        console.error('Max reconnect attempts reached. Unable to reconnect.');
    }
};

// Export the received message ref and the necessary functions
export default {
    receivedMessage,
    initializeWebSocket,
    sendMessage,
};
