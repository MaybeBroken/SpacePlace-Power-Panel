document.addEventListener('DOMContentLoaded', function () {
    let socket;
    const statusElem = document.getElementById('websocket-connected-status');
    const WS_URL = 'ws://localhost:8765';

    function connectWebSocket() {
        socket = new WebSocket(WS_URL);

        socket.onopen = function () {
            console.log("WebSocket connection established");
            statusElem.style.backgroundColor = 'green';
        };

        socket.onmessage = function (event) {
            console.log("Received message:", event.data);
        };

        socket.onclose = function () {
            console.log("WebSocket connection closed, retrying...");
            statusElem.style.backgroundColor = 'red';
            setTimeout(connectWebSocket, 2000); // Retry after 2 seconds
        };

        socket.onerror = function () {
            // Optional: close socket on error to trigger reconnect
            socket.close();
        };
    }

    connectWebSocket();
});