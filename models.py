from collections import UserString
import json


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


class Record:
    def __init__(self, name, phones):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]

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
                    Name(user_dict["name"]),
                    [Phone(phone) for phone in user_dict["phones"]],
                )
            else:
                raise ValueError("Parsed data is not a valid user dictionary.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON data: {e}")

    def to_json(self):
        user_dict = {
            "name": str(self.name),
            "phones": [str(phone) for phone in self.phones],
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

    def __str__(self):
        phones_str = ", ".join(str(phone) for phone in self.phones)
        return f"{self.name}: {phones_str}"

    def __repr__(self):
        phones_str = ", ".join(str(phone) for phone in self.phones)
        return f"Record({self.name}, [{phones_str}])"

    def __eq__(self, other):
        return self.name == other.name and self.phones == other.phones

    def __ne__(self, other):
        return not self == other
