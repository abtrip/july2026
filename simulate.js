const { io } = require('socket.io-client');

// TARGET SETTINGS
const SERVER_URL = process.env.WEB_PUBSUB_ENDPOINT || 'https://<your-service-name>.webpubsub.azure.com';
const CONTAINER_ID = process.env.CONTAINER_ID || '0';
const TOTAL_CLIENTS = 40000; 
const CLIENT_BATCH_SIZE = 50; 
const BATCH_INTERVAL_MS = 25; 

let connectedCount = 0;

function createClient(index) {
    const socket = io(SERVER_URL, {
        path: "/clients/socketio/hubs/Hub",
        transports: ['websocket'],
        rememberUpgrade: true,
        reconnection: false
    });

    socket.on('connect', () => {
        connectedCount++;
        if (connectedCount === TOTAL_CLIENTS) {
            console.log(`[ACI-${CONTAINER_ID}] Complete! Spawned all ${TOTAL_CLIENTS} sockets.`);
        }
    });

    socket.on('disconnect', () => {
        connectedCount--;
    });
}

console.log(`Starting execution for ACI Instance #${CONTAINER_ID}...`);
let currentClientIndex = 0;
const interval = setInterval(() => {
    for (let i = 0; i < CLIENT_BATCH_SIZE; i++) {
        if (currentClientIndex >= TOTAL_CLIENTS) {
            clearInterval(interval);
            break;
        }
        createClient(currentClientIndex);
        currentClientIndex++;
    }
}, BATCH_INTERVAL_MS);

// Keep process alive indefinitely for persistent load monitoring
setInterval(() => {
    console.log(`[ACI-${CONTAINER_ID}] Live Status Count: ${connectedCount}/${TOTAL_CLIENTS} persistent links active.`);
}, 10000);
