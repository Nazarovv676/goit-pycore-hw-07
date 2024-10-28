from collections import UserString
import json
import re


class Field(UserString):
    """
    Base class for user data fields.
    """

    pass


class Name(Field):
    """
    Class for user name field.
    """

    pass


class Phone(Field):
    """
    Class for user phone field.

    Raises:
        ValueError: If phone number is not a 10-digit number
    """

    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)


class Birthday(Field):
    """
    Class for user birthday field.

    Raises:
        ValueError: If birthday is not in DD.MM.YYYY format
    """

    def __init__(self, birthday):
        if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", birthday):
            raise ValueError("Birthday must be in DD.MM.YYYY format.")

        super().__init__(birthday)


class Record:
    def __init__(self, name, phones, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]
        self.birthday = Birthday(birthday) if birthday else None

    @staticmethod
    def from_json(json_str):
        try:
            user_dict = json.loads(json_str)
            if (
                isinstance(user_dict, dict)
                and "name" in user_dict
                and "phones" in user_dict
            ):
                return Record(
                    name=user_dict["name"],
                    phones=user_dict["phones"],
                    birthday=user_dict.get("birthday"),
                )
            else:
                raise ValueError("Parsed data is not a valid user dictionary.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON data: {e}")

    def to_json(self):
        user_dict = {
            "name": str(self.name),
            "phones": [str(phone) for phone in self.phones],
            "birthday": str(self.birthday) if self.birthday else None,
        }
        return json.dumps(user_dict)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p != Phone(phone)]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        return phone in self.phones

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = ", ".join(str(phone) for phone in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"{self.name}: {phones_str}{birthday_str}"

    def __repr__(self):
        phones_str = ", ".join(str(phone) for phone in self.phones)
        birthday_str = f", {self.birthday}" if self.birthday else ""
        return f"Record({self.name}, [{phones_str}]{birthday_str})"

    def __eq__(self, other):
        if not isinstance(other, Record):
            return False
        return (
            self.name == other.name
            and self.phones == other.phones
            and self.birthday == other.birthday
        )

    def __ne__(self, other):
        return not self == other
