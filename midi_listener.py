import mido


def start_midi_handshake():
    print("\n--- AUDIO SECURITY PROTOCOL INITIATED ---")
    print("CONNECT INTERFACE CABLE TO PORT: [PIANO]")

    # 1. LIST PORTS (To help you debug)
    input_names = mido.get_input_names()
    if not input_names:
        print("ERROR: NO MIDI DEVICE DETECTED. CHECK CABLE CONNECTION.")
        return False

    # We'll just grab the first device found for simplicity,
    # or you can look for "USB" in the name
    device_name = input_names[0]
    print(f"DEVICE DETECTED: {device_name}")
    print("WAITING FOR PASS-PHRASE SEQUENCE...")

    # 2. DEFINE THE SECRET MELODY (Middle C is 60)
    # Example: C, E, G, High C (C Major Arpeggio)
    # MIDI Note Numbers: 60, 64, 67, 72
    secret_melody = [60, 64, 67, 72]
    user_input_buffer = []

    # 3. LISTEN LOOP
    try:
        with mido.open_input(device_name) as inport:
            for msg in inport:
                # Filter for "Note On" events with velocity > 0
                if msg.type == 'note_on' and msg.velocity > 0:
                    print(f"NOTE RECEIVED: {msg.note}")  # Optional: Feedback on screen

                    user_input_buffer.append(msg.note)

                    # Keep buffer same size as secret melody
                    if len(user_input_buffer) > len(secret_melody):
                        user_input_buffer.pop(0)

                    # Check for match
                    if user_input_buffer == secret_melody:
                        print("\n*** ACCESS GRANTED ***")
                        print("Melody Confirmed: The Song of Storms")
                        return True

    except KeyboardInterrupt:
        print("\nABORTING HANDSHAKE...")
        return False


def main():
    start_midi_handshake()

# You can test this by running start_midi_handshake()
if __name__ == "__main__":
    main()