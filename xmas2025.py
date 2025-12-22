from colorama import Fore, Style
import os
from enum import Enum
# import pygame
# from tkinter import Tk, Label
# from PIL import Image, ImageTk

ascii_logo = r"""
  ____ _          _     _                       
 / ___| |__  _ __(_)___| |_ _ __ ___   __ _ ___ 
| |   | '_ \| '__| / __| __| '_ ` _ \ / _` / __|
| |___| | | | |  | \__ \ |_| | | | | | (_| \__ \
 \____|_| |_|_|  |_|___/\__|_| |_| |_|\__,_|___/
                                                
 ____            _                 _                  
|  _ \  __ _  __| |_   _____ _ __ | |_ _   _ _ __ ___ 
| | | |/ _` |/ _` \ \ / / _ \ '_ \| __| | | | '__/ _ \
| |_| | (_| | (_| |\ V /  __/ | | | |_| |_| | | |  __/
|____/ \__,_|\__,_| \_/ \___|_| |_|\__|\__,_|_|  \___|
                                                      
 ____   ___ ____  _  _   
|___ \ / _ \___ \| || |  
  __) | | | |__) | || |_ 
 / __/| |_| / __/|__   _|
|_____|\___/_____|  |_|  """

# pygame.mixer.init()
# morse = pygame.mixer.Sound('morsecode.wav')

class C_Puzzles(Enum):
    Moon = 1,
    Baker = 2

c_solved = 0
e_solved = 0
l_solved = 0
j_solved = 0
d_solved = 0
intro_message_displayed = False

current_user = ""
users = "C007", "L00tB0x", "MeatHook", "TheEld3r", "3rdHead"

intro_message = "\"Agents C, L and E—\n\n" \
"Her Majesty’s Trust has selected you for a matter of extreme delicacy and national importance.\n" \
"There exists a powerful computer program known as the Starlight Core, a source of great mystery and magic.\n" \
"It has been compromised by an unknown adversary with the moniker ‘Frostbyte.’\n\n" \
"Our intelligence suggests that the Starlight Core's unlock codes have been scattered and hidden behind a series of\n" \
"ingenious locks, codes, and ancient relics. You must retrieve them before the hour grows too late.\n\n" \
"Enclosed are your mission dossiers. Proceed with utmost discretion, for dark forces would see you fail.\n" \
"Trust only your closest allies, and remember: in service to the Crown, one must rise above the ordinary.\n\n" \
"May fortune favor the bold.\n\n" \
"Signed,\n" \
"Lord Pembroke\n" \
"Keeper of the Pantry, Royal Intelligence Bureau\""
c_moon_clue = "When shadows stretch and stars ignite,\nSeek the orb that guards the night.\nIts glow conceals what you require,\nA key named for celestial fire."
c_dwarf_clue = "Through mountain halls where stone kings dwell,\nSeek the cup of dwarves that legends tell.\nStrong of arm, stout of heart—\nFind this relic to play your part."
c_anne_clue = "\033[3mDear Kindred Spirit,\033[0m\nI’ve hidden a secret among the pages of a book that speaks of dreams, stubborn hearts, and kindred souls. Seek where I learned that the right path is often ‘the bend in the road.’"
c_starlight_clue = "TOP-SECRET ROYAL DISPATCH\nOPERATION: Silent Nightfall\nClassification: Ultra Secure - Eyes Only\n\n" \
                        "Directive:\n\nAgent C,\n\nThe encrypted Starlight Document must be transferred under utmost secrecy. Her Majesty’s Intelligence Bureau has designated Agent E as the sole authorized courier.\n\n" \
                        "Failure to execute this handoff with precision could compromise the entire mission. Be advised that Frostbyte's operatives remain at large. Proceed with caution. Trust no one but Agent E.\n\n" \
                        "By Order of the Crown,\nLord Pembroke\nKeeper of the Pantry, Royal Intelligence Bureau"
c_final_code = "A, M"
l_rna_clue = "TOP SECRET BIOLOGICAL THREAT FILE\nMission: Neutralize the Invading Pathogen\n\n"\
             "A foreign pathogen has breached Her Majesty's biological defenses. Our intelligence indicates that the only way to create an effective antibody is by finding the correct sequence of amino acids.\n"\
             "Use the encoded mRNA sequence provided below to build the exact 4-letter antibody codename and submit it at the terminal. Failure is not an option.\n" \
             "mRNA SEQUENCE: GGU - GCU - UCU - CCU" # TODO print
l_b4_clue = "Classified Mission Report\nStormwarden Command – Urgent Dispatch\n" \
                "Agent L-,\n\nA critical operation has emerged from the shattered plains. You are tasked with locating the ancient text where \"men became more than tools\" and \"stood together as one.\"\n" \
                "Seek the moment when the bridgemen found purpose and became something greater than themselves.\nThe chapter you seek will guide you toward unity and strength.\n\n" \
                "Remember: The most important step a man can take is always the next one.\n\n May the Stormfather watch over you.\n\n" \
                "Signed,\nHighstorm Intelligence Bureau (HIB)"
l_pirate_clue = "Bridgeman’s Secret Orders\n\nHonor is not in the title but in the strength of one's crew.\n\n" \
                    "You’ve earned your place among Bridge Four, but your mission doesn’t end here. Seek the “Captain's Crown”, worn by only the boldest of storm-chasers and sky-raiders.\nIts brim still carries the salt of distant seas and the memory of windswept battles." \
                    "Signed,\nCaptain Stormseye, Sky Raider of the Shattered Plains" # TODO
l_final_code = "H, T"

e_buddha_clue = "Agent E,\nTo unlock the first piece of the Starlight Core Code, you must seek wisdom from the Three Silent Guardians.\n" \
                    "One of Rock, One of Wood, One of Soapstone\nBeneath their watchful gaze, secrets unfold.\n\n" \
                    "They sit in stillness and serenity, guarding the fragments of what you seek.\nTurn them over and collect all three parts to complete the first key.\n\n" \
                    "But beware: Only when their wisdom is combined will the true path be revealed.\n\nSigned,\nLord Pembroke\nKeeper of the Sacred Relics"

e_final_code = "S, E"

def main():

    clear_terminal()
    # show_image("frostbyte.png")

    center_text(ascii_logo, Fore.WHITE)
    center_text("\n\nOperation: Silent Nightfall", Fore.RED)
    print(Fore.GREEN + "\n\nYou are now entering a secure channel..." + Style.RESET_ALL)

    while True:
        print(f"Welcome: {Style.BRIGHT + current_user}")
        print(Fore.RED + "1. Enter a secret agent code" + Style.RESET_ALL)
        print(Fore.GREEN + "2. Receive Your Mission Briefing" + Style.RESET_ALL)
        print(Fore.YELLOW + "3. Enter a Secret Code" + Style.RESET_ALL)

        choice = input("Enter the number of your choice: ")

        if choice == "1":
            a_code = input("Enter your agent code: " + Style.RESET_ALL)
            enter_agent_code(a_code)
        elif choice == "2":
            enter_secret_code()
        elif choice == "3":
            print(Fore.RED + "Mission Terminated. Stay vigilant, Agent." + Style.RESET_ALL)
            break
        else:
            print(Fore.YELLOW + "Invalid choice. Please select a valid mission." + Style.RESET_ALL)

def show_image(image_path):
    # Create the Tkinter window
    root = Tk()
    root.title("Image Viewer")

    # Load the image using Pillow
    image = Image.open(image_path)
    img = ImageTk.PhotoImage(image)

    # Create a Label to display the image
    label = Label(root, image=img)
    label.pack()

    # Run the Tkinter event loop
    root.mainloop()

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Mac and Linux
    else:
        os.system('clear')

def center_text(ascii_art, color):
    terminal_width = os.get_terminal_size().columns
    for line in ascii_art.splitlines():
        print(color + line.center(terminal_width))
    print("\n" + Style.RESET_ALL)

def receive_briefing(agent_code):
    match agent_code:
        case "C007":
            print_fancy_message("test")
        case "L00tB0x":
            print_fancy_message("test")
        case "MeatHook":
            print_fancy_message("test")
        case "TheEld3r":
            print_fancy_message("test")
        case "Cerberus":
            print_fancy_message("test")
        case _:
            print("Sir, this is a Wendy's.")

def enter_agent_code(agent_code):
    global intro_message_displayed
    global current_user
    current_user = agent_code
    match agent_code:
        case "C007":
            if not intro_message_displayed:
                print_fancy_message(intro_message)
                intro_message_displayed = True
        case "L00tB0x":
            if not intro_message_displayed:
                print_fancy_message(intro_message)
                intro_message_displayed = True
        case "MeatHook":
            if not intro_message_displayed:
                print_fancy_message(intro_message)
                intro_message_displayed = True
        case "TheEld3r":
            if not intro_message_displayed:
                print_fancy_message(intro_message)
                intro_message_displayed = True
        case "Cerberus":
            if not intro_message_displayed:
                print_fancy_message(intro_message)
                intro_message_displayed = True
        case _:
            print("Sir, this is a Wendy's.")


def mission_briefing():
    print("\n--- Mission Briefing ---")
    print(Fore.CYAN + "Agent C," + Style.RESET_ALL)
    print("You have been selected for a mission of extreme importance.")
    print(Fore.MAGENTA + "Retrieve the Starlight Core before the enemy, Frostbyte, strikes." + Style.RESET_ALL)
    print("Your first clue is waiting... trust no one but your team.")
    print(Fore.GREEN + "Good luck." + Style.RESET_ALL)

def print_fancy_message(body_text):
    header = "---SECURE CHANNEL 005. OPERATION STARLIGHT SAVIOR---"
    body = (
        Fore.CYAN + "Message from: Lord Pembroke, Keeper of the Pantry, Royal Intelligence Bureau" + Style.RESET_ALL + "\n\n" + body_text
    )
    footer = "---END TRANSMISSION---"

    clear_terminal()
    print()
    center_text(header, Fore.YELLOW)
    print()
    center_text(body, Fore.WHITE)
    print()
    center_text(footer, Fore.RED)


def enter_secret_code():
    match current_user:
        case "C007":
            if c_solved == 0:
                code = input(Fore.CYAN + "\nEnter a secret code: " + Style.RESET_ALL)
                if code.lower() == "lunar":
                    print(Fore.GREEN + "Through mountain halls where stone kings dwell,\nSeek the cup of dwarves that legends tell.\nStrong of arm, stout of heart\nFind this relic to play your part." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Access Denied. Incorrect code. The mission depends on you!" + Style.RESET_ALL)




if __name__ == "__main__":
    # main()
    pass


