import { ref } from 'vue';

let ws;
let reconnectAttempts = 0;

// Create a reactive ref to store the received message
const receivedMessage = ref(null);

// Helper function to get current timestamp
const getTimestamp = () => {
    return new Date().toISOString();
};

// Modified log function to add timestamps
const logWithTimestamp = (level, message) => {
    console[level](`[websocketService.js] [${getTimestamp()}] ${message}`);
};

const initializeWebSocket = () => {
    logWithTimestamp('log', 'Initializing WebSocket connection...');
    ws = new WebSocket('ws://' + import.meta.env.VITE_SERVER_URL + '/ws/client');

    ws.onopen = () => {
        logWithTimestamp('log', 'WebSocket Connected');
        reconnectAttempts = 0;
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            logWithTimestamp('log', `Received message: ${JSON.stringify(data)}`);
            receivedMessage.value = data;
        } catch (error) {
            logWithTimestamp('error', `Error parsing message: ${error}`);
        }
    };

    ws.onclose = () => {
        logWithTimestamp('log', 'WebSocket Disconnected');
        attemptReconnect();
    };

    ws.onerror = (error) => {
        logWithTimestamp('error', `WebSocket Error: ${error}`);
        ws.close(); // Ensure it's closed before attempting reconnection
    };
};

const sendMessage = (action, message, recipient = 'server') => {
    if (ws?.readyState === WebSocket.OPEN) {
        try {
            logWithTimestamp('log', `Sending message: { action: ${action}, message: ${message}, recipient: ${recipient} }`);
            ws.send(JSON.stringify({
                from: 'client',
                to: recipient,
                action: action,
                message: message
            }));
        } catch (error) {
            logWithTimestamp('error', `Error sending message: ${error}`);
        }
    } else {
        logWithTimestamp('warn', `WebSocket not open. Message not sent: ${message}`);
    }
};

const attemptReconnect = () => {
    if (reconnectAttempts < 5) {
        setTimeout(() => {
            logWithTimestamp('log', `Attempting to reconnect... (${reconnectAttempts + 1})`);
            reconnectAttempts++;
            initializeWebSocket();
        }, 2000 * reconnectAttempts); // Backoff delay (e.g., 2s, 4s, 6s, etc.)
    } else {
        logWithTimestamp('error', 'Max reconnect attempts reached. Unable to reconnect.');
    }
};

// Export the received message ref and the necessary functions
export default {
    receivedMessage,
    initializeWebSocket,
    sendMessage,
};
