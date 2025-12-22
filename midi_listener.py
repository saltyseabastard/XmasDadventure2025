import mido
import os
from colorama import Fore, Style

def start_midi_handshake():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.GREEN}\n--- AUDIO SECURITY PROTOCOL INITIATED ---")
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
    secret_melody = [57, 60, 64, 69]
    secret_melody_2 = [69, 72, 76, 81]
    chronos_protocol = [60, 69, 63, 66]
    chronos_protocol_2 = [60, 69, 75, 89]
    chronos_protocol_3 = [48, 57, 51, 54]
    chronos_protocol_4 = [48, 57, 63, 66]


    user_input_buffer = []

    # 3. LISTEN LOOP
    try:
        with mido.open_input(device_name) as inport:
            for msg in inport:
                # Filter for "Note On" events with velocity > 0
                if msg.type == 'note_on' and msg.velocity > 0:
                    print(f"{Fore.GREEN} NOTE RECEIVED: {msg.note}")  # Optional: Feedback on screen

                    user_input_buffer.append(msg.note)

                    # Keep buffer same size as secret melody
                    if len(user_input_buffer) > len(secret_melody):
                        user_input_buffer.pop(0)

                    # Check for match
                    if user_input_buffer == secret_melody or user_input_buffer == secret_melody_2:
                        print(f"{Fore.WHITE}\n*** ACCESS GRANTED ***")
                        print(f"CODE: {Fore.YELLOW} AMPLITUDE")
                        user_input_buffer.clear()
                        
                        # clear terminal
                        #os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"{Fore.GREEN}\n\n\nWAITING FOR NEXT PASS-PHRASE SEQUENCE...")

                    elif user_input_buffer == chronos_protocol or user_input_buffer == chronos_protocol_2 or user_input_buffer == chronos_protocol_3 or user_input_buffer == chronos_protocol_4:
                        print(f"{Fore.WHITE}\n*** ACCESS GRANTED ***")
                        print(f"CODE: {Fore.YELLOW}MODULATION\n\n\n")
                        user_input_buffer.clear()

                        return True




    except KeyboardInterrupt:
        print("\nABORTING HANDSHAKE...")
        return False


def main():
    start_midi_handshake()

# You can test this by running start_midi_handshake()
if __name__ == "__main__":
    main()