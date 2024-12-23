import pyfiglet


def generate_ascii_text():
    print("Welcome to the ASCII Text Generator!\n")

    while True:
        text = input("Enter the text you want to convert to ASCII (or type 'exit' to quit): ")
        if text.lower() == 'exit':
            print("Goodbye!")
            break

        font = input("Enter the font style (leave blank for default): ")

        try:
            ascii_art = pyfiglet.figlet_format(text, font=font if font else "standard")
            print("\nHere is your ASCII text:\n")
            print(ascii_art)
        except pyfiglet.FontNotFound:
            print("Invalid font name. Please try again.\n")


if __name__ == "__main__":
    generate_ascii_text()