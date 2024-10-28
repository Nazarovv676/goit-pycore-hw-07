from tabulate import tabulate
from models import Name, Phone, Record
from input_error_handler import input_error
from address_book import AddressBook


_address_book = AddressBook()


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
    
    add-birthday <name> <birthday> Adds a birthday for the specified user.
    
    show-birthday <name>      Retrieves the birthday of the specified user.
    
    birthdays                 Displays upcoming birthdays (in a week).

    help                      Displays this help message.

    close / exit              Exits the application.
"""
    return help_text


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


@input_error(
    "🤖\tPlease provide the name and birthday.\n\tUsage: `add-birthday <name> <birthday>`\n\tExample: `add-birthday John DD.MM.YYYY`."
)
def add_birthday(name, birthday):
    _address_book.add_birthday(name, birthday)

    return f"🤖\tBirthday added for '{name}'."


@input_error(
    "🤖\tPlease provide the name.\n\tUsage: `show-birthday <name>`\n\tExample: `show-birthday John`."
)
def get_birthday(name):
    user = _address_book.find(name)
    birthday = user.birthday

    return f"🤖\tUser birthday: '{str(birthday)}'."


# get upcoming birthdays
@input_error("🤖\tSorry... Some error occurred when retrieving users.")
def get_upcoming_birthdays():
    users = _address_book.get_upcoming_birthdays()
    table_data = [(user["name"], user["congratulation_date"]) for user in users]

    return tabulate(
        table_data, headers=["Name", "Congratulation date"], tablefmt="fancy_grid"
    )
