import os
from colorama import init, Fore, Style
import hacker_attack

ascii_title = r"""
 ___  ___  ________  ________  ___  __    _______   ________          ________  _________  _________  ________  ________  ___  __       
|\  \|\  \|\   __  \|\   ____\|\  \|\  \ |\  ___ \ |\   __  \        |\   __  \|\___   ___\\___   ___\\   __  \|\   ____\|\  \|\  \     
\ \  \\\  \ \  \|\  \ \  \___|\ \  \/  /|\ \   __/|\ \  \|\  \       \ \  \|\  \|___ \  \_\|___ \  \_\ \  \|\  \ \  \___|\ \  \/  /|_   
 \ \   __  \ \   __  \ \  \    \ \   ___  \ \  \_|/_\ \   _  _\       \ \   __  \   \ \  \     \ \  \ \ \   __  \ \  \    \ \   ___  \  
  \ \  \ \  \ \  \ \  \ \  \____\ \  \\ \  \ \  \_|\ \ \  \\  \|       \ \  \ \  \   \ \  \     \ \  \ \ \  \ \  \ \  \____\ \  \\ \  \ 
   \ \__\ \__\ \__\ \__\ \_______\ \__\\ \__\ \_______\ \__\\ _\        \ \__\ \__\   \ \__\     \ \__\ \ \__\ \__\ \_______\ \__\\ \__\
    \|__|\|__|\|__|\|__|\|_______|\|__| \|__|\|_______|\|__|\|__|        \|__|\|__|    \|__|      \|__|  \|__|\|__|\|_______|\|__| \|__|

                                                                                                         """

init()

def render_ui(game, question, prev_status):
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{Fore.RED}SYSTEM BREACH DETECTED!\nYou must defend against the...\n{ascii_title}{Style.RESET_ALL}\n")

    if prev_status:
        print(prev_status)
        print()

    # progress bar
    answered = getattr(game, "answered_count", 0)
    max_q = getattr(game, "max_questions", 10) or 10
    width = 30
    filled = int((answered / max_q) * width) if max_q else 0
    bar = "[" + "#" * filled + "-" * (width - filled) + "]"
    print(f"Progress: {bar} {answered}/{max_q}\n")

    print(f"{Fore.RED}{question}{Style.RESET_ALL}\n")


def hacker():
    game = hacker_attack.HackerGame()
    question, status = game.start_game()
    prev_status = ""

    while status != "COMPLETE":
        render_ui(game, question, prev_status)

        # prompt with white input text; reset colors after reading
        user_answer = input(f"{Fore.WHITE}Input answer: ")
        print(Style.RESET_ALL, end="")

        correct = game.check_answer(user_answer)
        if correct:
            prev_status = f"{Fore.YELLOW}CORRECT!{Style.RESET_ALL}"
        else:
            prev_status = f"{Fore.RED}INCORRECT! Frostbyte has breached another layer of your system!{Style.RESET_ALL}"

        # fetch next question/status
        question, status = game.next_question()

    # final screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.GREEN}🎉 SYSTEM SECURED! You have successfully defended against the hacker attack! 🎉{Style.RESET_ALL}")


def main():
    hacker()


if __name__ == "__main__":
    main()
