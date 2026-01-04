from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pegasus-pulse-secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

def stream_command(command, event_name):
    """Stream command output to connected clients"""
    while True:
        try:
            # Run the command and capture output
            if command == 'htop':
                # Use top instead of htop for better compatibility in non-interactive mode
                process = subprocess.Popen(
                    ['top', '-b', '-n', '1'],
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                process = subprocess.Popen(
                    command.split(),
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            output, error = process.communicate()
            
            if error:
                socketio.emit(event_name, {'data': f'Error: {error}'})
            else:
                socketio.emit(event_name, {'data': output})
            
            time.sleep(2)  # Update every 2 seconds
            
        except Exception as e:
            socketio.emit(event_name, {'data': f'Exception: {str(e)}'})
            time.sleep(5)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'data': 'Connected to Pegasus Pulse'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('start_streams')
def handle_start_streams():
    # Start streaming threads
    threading.Thread(target=stream_command, args=('htop', 'htop_output'), daemon=True).start()
    threading.Thread(target=stream_command, args=('docker ps', 'docker_output'), daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)