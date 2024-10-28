import command_parser
import command_handler


def main():
    print("Welcome to the assistant bot version 1.0!")
    command_handler.show_help()

    status_code = 0
    while status_code == 0:
        command = input(">>>\t")
        status_code = command_parser.parse(command)


if __name__ == "__main__":
    main()
