from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import puzzles_2025 as PUZZLES

# Initialize Flask App
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'secret_key_xmas_2025'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# Game Logic

class GameEngine:
    def __init__(self):
        self.logs = []
        # We no longer track specific users, strictly shared state
    
    def log(self, message, color="white", exclude_sid=None):
        # Strip ANSI codes if present (simple regex)
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_message = ansi_escape.sub('', str(message))
        
        self.logs.append({"text": clean_message, "color": color})
        if len(self.logs) > 50:
            self.logs.pop(0)
        # If exclude_sid is provided, skip sending to that socket to avoid duplicate local echo.
        if exclude_sid:
            socketio.emit('new_log', {"text": clean_message, "color": color}, skip_sid=exclude_sid)
        else:
            socketio.emit('new_log', {"text": clean_message, "color": color})

    def handle_command(self, cmd, source="TERMINAL"):
        cmd = cmd.strip()
        self.log(f"{source}> {cmd}", "green")
        
        cmd_lower = cmd.lower()
        
        if cmd_lower == "help":
            self.log("SYSTEM: Search for hidden codes. Type anything to attempt decryption.", "yellow")
            return

        elif cmd_lower == "clear":
             # Frontend handles clear often, but we can respect it
             pass

        # Check Puzzles
        found = False
        for puzzle in PUZZLES.PUZZLES:
            if cmd_lower in [p.lower() for p in puzzle['patterns']]:
                self.log("\n\n\n>>> MATCH CONFIRMED <<<", "cyan")
                self.log(puzzle['message'], "white")
                found = True
                break
        
        if not found:
             self.log("Pattern mismatch. Scanning...", "grey")

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

# @app.route('/midi')
# def midi_terminal():
#     return render_template('midi.html')

@socketio.on('connect')
def handle_connect():
    emit('init_logs', game.logs)
    if not game.logs:
        game.log("System Online. Waiting for input...", "grey")


# ... (Existing imports)

# Initialize Hacker Games State
hacker_sessions = {} # sid -> HackerGame instance

# @app.route('/hacker')
# def hacker_terminal():
#     return render_template('hacker.html')

# ... (Existing Routes) ...

# @socketio.on('hacker_init')
# def handle_hacker_init():
#     sid = request.sid
#     hacker_sessions[sid] = HackerGame()
#     problem, status = hacker_sessions[sid].start_game()
#     emit('hacker_problem', {'problem': problem, 'current': 0, 'total': 10})

@socketio.on('command')
def handle_command(data):
    cmd = data.get('command')
    # sid = request.sid
    
    # 1. Redirection Logic (Check global commands first)
    # if cmd.lower() in ['hacker', 'hack']:
    #     emit('redirect', {'url': '/hacker'})
    #     return
    # if cmd.lower() in ['midi', 'audio']:
    #     emit('redirect', {'url': '/midi'})
    #     return
    if cmd.lower() in ['terminal', 'main', 'exit']:
        emit('redirect', {'url': '/'})
        return

    # 2. Hacker Mode Logic
    # If the user is on the /hacker page, they will be sending commands here too.
    # We need a way to know WHICH page they are on, OR we treat all input as potential answers if a session exists?
    # Better: If referer header indicates /hacker? Or just check if SID has active hacker game?
    
    # Simplification: If /hacker page is open, the client sends 'command'. 
    # But wait, existing script.js sends 'command'. 
    # Let's check if this SID is in hacker_sessions AND the input looks like a number?
    # OR better, if they are on /hacker, use a DIFFERENT event?
    # I'll rely on the redirect logic above: if they are on /hacker, they won't type "hacker".
    
    # Actually, let's distinguish by checking if they are in a hacker session loop.
    # referer = request.headers.get('Referer')
    # if referer and 'hacker' in referer:
    #     # HACKER GAME LOOP
    #     if sid not in hacker_sessions:
    #         hacker_sessions[sid] = HackerGame()
    #         hacker_sessions[sid].start_game()
    #
    #     hg = hacker_sessions[sid]
    #     if hg.check_answer(cmd):
    #         # Correct
    #         prob, status = hg.next_question()
    #         if status == "COMPLETE":
    #             emit('hacker_complete', {})
    #             del hacker_sessions[sid]
    #         else:
    #             print("Sending problem: " + prob)
    #             emit('hacker_problem', {'problem': prob, 'current': hg.question_count, 'total': hg.max_questions})
    #     else:
    #         # Incorrect - just flash or stay same
    #         emit('new_log', {"text": "INCORRECT CALCULATION", "color": "red"})
    #     return

    # 3. Standard Game Logic (Main Terminal)
    game.handle_command(cmd, source="TERMINAL")

# @socketio.on('midi_note')
# def handle_midi(data):
#     secret_melody = [57, 60, 64, 69]
#     secret_melody_2 = [69, 72, 76, 81]
#     chronos_protocol = [60, 69, 63, 66]
#     chronos_protocol_2 = [60, 69, 75, 89]
#     chronos_protocol_3 = [48, 57, 51, 54]
#     chronos_protocol_4 = [48, 57, 63, 66]
#
#     note = data.get('note')
#     #velocity = data.get('velocity')
#
#     # Optional: Log specific notes or just hidden melody progress
#     #game.log(f"MIDI SIGNAL DETECTED: {note}", "magenta")
#
#     # Check for Secret Melody (C Major Arp: 60, 64, 67, 72)
#     # This is a basic example of matching a sequence
#     if not hasattr(game, 'midi_buffer'):
#         game.midi_buffer = []
#
#     # Exclude the sender when broadcasting this transient MIDI tick so the sender doesn't see a duplicated line
#     game.log(f"MIDI SIGNAL DETECTED: {note}", "magenta", exclude_sid=request.sid)
#     game.midi_buffer.append(note)
#     if len(game.midi_buffer) > 4:
#         game.midi_buffer.pop(0)
#
#     game.log(game.midi_buffer)
#     if game.midi_buffer == secret_melody or game.midi_buffer == secret_melody_2:
#         game.log(">>> AUDIO SECURITY BYPASSED<<<", "green")
#         game.log("CODE: AMPLITUDE", "white")
#         game.midi_buffer = [] # Reset

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
