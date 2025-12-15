import xmas2024
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import os
import eventlet

# Initialize Flask App
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'secret_key_xmas_2025'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# Game State Management
class GameEngine:
    def __init__(self):
        self.logs = []
        self.connected_users = {}  # sid -> agent_code

    def log(self, message, color="white"):
        # Strip ANSI codes if present (simple regex)
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_message = ansi_escape.sub('', message)
        
        self.logs.append({"text": clean_message, "color": color})
        if len(self.logs) > 50:
            self.logs.pop(0)
        socketio.emit('new_log', {"text": clean_message, "color": color})

    def handle_command(self, cmd, sid):
        cmd = cmd.strip()
        user = self.connected_users.get(sid, "UNKNOWN")
        
        self.log(f"{user}> {cmd}", "green")
        
        # Parse Commands
        cmd_lower = cmd.lower()
        if cmd_lower == "help":
            self.log("COMMANDS:", "yellow")
            self.log("  AGENT [CODE] - Log in", "white")
            self.log("  SOLVE [CODE] - Submit solution", "white")
            self.log("  CLEAR - Clear screen", "white")
        
        elif cmd_lower.startswith("agent "):
            code = cmd.split(" ", 1)[1]
            if code in xmas2024.users:
                self.connected_users[sid] = code
                self.log(f"Identity Verified: Agent {code}", "cyan")
                # Send briefing
                self.log(xmas2024.intro_message, "white")
            else:
                self.log("Access Denied. Invalid Agent Code.", "red")

        elif cmd_lower.startswith("solve "):
            attempt = cmd.split(" ", 1)[1].lower()
            # Basic Logic Mapping from xmas2024.py
            # Note: This is a simplified port. Ideally we'd map puzzles more robustly.
            if attempt == "lunar":
                self.log(xmas2024.c_dwarf_clue, "cyan")
            elif attempt == xmas2024.c_final_code.lower():
                self.log("Correct! Sector C Cleared.", "green")
            else:
                 self.log("Incorrect Code.", "red")

        elif cmd_lower == "clear":
             # Frontend handles clear, but we can reset logs?
             pass
        else:
             self.log(f"Unknown command: {cmd}", "grey")

game = GameEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('.', filename)

@socketio.on('connect')
def handle_connect():
    emit('init_logs', game.logs)
    game.log("New connection established...", "grey")

@socketio.on('command')
def handle_command(data):
    cmd = data.get('command')
    game.handle_command(cmd, request.sid)

@socketio.on('midi_note')
def handle_midi(data):
    note = data.get('note')
    velocity = data.get('velocity')
    user = game.connected_users.get(request.sid, "Unknown")
    game.log(f"MIDI SIGNAL: {note} (Vel: {velocity}) from {user}", "magenta")
    
    # Check for Secret Melody (C Major Arp: 60, 64, 67, 72)
    # Basic shared buffer logic could go here

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)


