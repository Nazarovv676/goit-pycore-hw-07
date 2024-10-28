from tabulate import tabulate
from models import Name, Phone, Record
from input_error_handler import input_error
from user_datasource import AddressBook


_address_book = AddressBook()


@input_error(
    "🤖\tGive me a name and phone number please.\n\tUsage: `add <name> <phone>`\n\tExample: `add John 1234567890`."
)
def add_user(name, phone):
    _address_book.add_record(Record(name, [phone]))

    return f"🤖\tUser '{name}' has been added."


@input_error(
    "🤖\tGive me a name and phone number please.\n\tUsage: `change <name> <phone>`\n\tExample: `change John 0987654321`."
)
def change_user(name, phone):
    _address_book.update_record(Record(name, [phone]))

    return f"🤖\tUser '{name}' has been changed."


@input_error(
    "🤖\tPlease provide the name.\n\tUsage: `phone <name>`\n\tExample: `phone John`."
)
def get_user_phone(name):
    user = _address_book.find(name)
    phones = user.phones

    return f"🤖\tUser phones: '{str(phones)}'."


@input_error("🤖\tSorry... Some error occurred when retrieving users.")
def get_all():
    users = _address_book.find_all()
    table_data = [(user.name, str.join("\n", map(str, user.phones))) for user in users]

    return tabulate(table_data, headers=["Name", "Phones"], tablefmt="fancy_grid")


def show_help():
    help_text = """
🤖 Command Line Tool

Usage:
    command [options]

Available Commands:
    add <name> <phone>        Adds a new user with the specified name and phone number.
                              Example: `add John 1234567890`

    change <name> <phone>     Updates the phone number of an existing user.
                              Example: `change John 0987654321`

    phone <name>              Retrieves the phone number of the specified user.
                              Example: `phone John`

    all                       Displays all users and their phone numbers.

    hello                     Greets the user and offers assistance.

    help                      Displays this help message.

    close / exit              Exits the application.
"""
    return help_text
