// Connect to WebSocket server
const socket = io();

// DOM elements
const statusElement = document.getElementById('status');
const htopOutput = document.getElementById('htop-output');
const dockerOutput = document.getElementById('docker-output');

// Connection handlers
socket.on('connect', () => {
    console.log('Connected to server');
    statusElement.textContent = '✓ Connected';
    statusElement.classList.add('connected');
    
    // Request to start streaming data
    socket.emit('start_streams');
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    statusElement.textContent = '✗ Disconnected';
    statusElement.classList.remove('connected');
});

socket.on('response', (data) => {
    console.log('Server response:', data.data);
});

// Handle htop output
socket.on('htop_output', (data) => {
    htopOutput.textContent = data.data;
    // Auto-scroll to bottom if user hasn't scrolled up
    if (htopOutput.scrollHeight - htopOutput.scrollTop < htopOutput.clientHeight + 100) {
        htopOutput.scrollTop = htopOutput.scrollHeight;
    }
});

// Handle docker ps output
socket.on('docker_output', (data) => {
    dockerOutput.textContent = data.data;
    // Auto-scroll to bottom if user hasn't scrolled up
    if (dockerOutput.scrollHeight - dockerOutput.scrollTop < dockerOutput.clientHeight + 100) {
        dockerOutput.scrollTop = dockerOutput.scrollHeight;
    }
});

// Error handling
socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
    statusElement.textContent = '✗ Connection Error';
    statusElement.classList.remove('connected');
});

socket.on('error', (error) => {
    console.error('Socket error:', error);
});
