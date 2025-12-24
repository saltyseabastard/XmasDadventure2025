document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const logsDiv = document.getElementById('logs');
    const inputField = document.getElementById('command-input');
    const screenDiv = document.querySelector('.screen');
    const cursor = document.querySelector('.cursor');

    // Focus input on click anywhere
    document.addEventListener('click', () => {
        inputField.focus();
    });

    // Handle Input
    inputField.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const command = inputField.value;
            if (command.trim() !== "") {
                socket.emit('command', { command: command, user: 'WEB_USER' }); // TODO: Agent ID
                inputField.value = '';
            }
        }
    });

    // Socket Events
    socket.on('redirect', (data) => {
        window.location.href = data.url;
    });

    socket.on('new_log', (data) => {
        appendLog(data.text, data.color);
    });

    socket.on('init_logs', (logs) => {
        logsDiv.innerHTML = '';
        logs.forEach(log => appendLog(log.text, log.color));
    });

    function appendLog(text, color) {
        const p = document.createElement('div');
        p.className = 'log-entry';
        p.style.color = colorMap(color);
        p.innerText = text; // Secure text content
        logsDiv.appendChild(p);
        screenDiv.scrollTop = screenDiv.scrollHeight;
    }

    function colorMap(colorName) {
        const colors = {
            'white': '#39ff14', // Default phosphor
            'red': '#ff3333',
            'green': '#39ff14',
            'yellow': '#ffff33',
            'cyan': '#33ffff',
            'grey': '#666666'
        };
        return colors[colorName] || colors['white'];
    }

    // Audio Context for Morse/Music (Can be triggered by server)
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    // TODO: Web MIDI Implementation
    // if (navigator.requestMIDIAccess) {
    //     navigator.requestMIDIAccess().then(onMIDISuccess, onMIDIFailure);
    // } else {
    //     appendLog("Web MIDI API not supported in this browser.", "red");
    // }
    //
    // function onMIDISuccess(midiAccess) {
    //     appendLog("MIDI System Initialized.", "green");
    //     for (var input of midiAccess.inputs.values()) {
    //         input.onmidimessage = getMIDIMessage;
    //     }
    // }
    //
    // function onMIDIFailure() {
    //     appendLog("Could not access your MIDI devices.", "red");
    // }

    // function getMIDIMessage(message) {
    //     var command = message.data[0];
    //     var note = message.data[1];
    //     var velocity = (message.data.length > 2) ? message.data[2] : 0;
    //
    //     // noteOn (typically 144)
    //     if (command === 144 && velocity > 0) {
    //         console.log("script.js says MIDI message received:", message.data);
    //         socket.emit('midi_note', { note: note, velocity: velocity });
    //     }
    // }
});
