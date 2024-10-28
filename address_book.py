from collections import UserList
from datetime import datetime, timedelta
import os
import tempfile
from models import Record


class DatabaseNotFoundError(Exception):
    """Custom exception raised when the database file is not found."""

    pass


class UserNotFoundError(Exception):
    """Custom exception raised when the user is not found."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"User '{self.name}' not found.")


class AddressBook(UserList):
    def __init__(
        self,
        db_path: str = "database.txt",
        file_encoding: str = "UTF-8",
        eol: str = "\n",
    ):
        """Initializes the address book and loads records from the file."""
        super().__init__()

        self._db_path = db_path
        self._file_encoding = file_encoding
        self._eol = eol

        self._load_data()

    def _load_data(self):
        """Loads records from the database file into the AddressBook."""
        if not os.path.exists(self._db_path):
            raise DatabaseNotFoundError("Database file not found.")
        with open(self._db_path, "r", encoding=self._file_encoding) as file:
            self.data = [Record.from_json(line.strip()) for line in file]

    def _persist_data(self):
        """Saves all records to the database file."""
        with open(self._db_path, "w", encoding=self._file_encoding) as file:
            for record in self.data:
                file.write(record.to_json() + self._eol)

    def add_record(self, user: Record):
        """Adds a new user to the address book and saves the database."""
        if not user:
            raise ValueError("Provide user info.")
        self.append(user)
        self._persist_data()

    def update_record(self, user: Record) -> Record:
        """Updates an existing user in the address book and saves the database."""
        if not user:
            raise ValueError("Provide user info.")
        for idx, record in enumerate(self.data):
            if record.name == user.name:
                self.data[idx] = user
                self._persist_data()
                return user
        raise UserNotFoundError(user.name)

    def find(self, name: str) -> Record:
        """Retrieves a user by their name."""
        if not name:
            raise ValueError("Provide user name.")
        for record in self.data:
            if record.name == name:
                return record
        raise UserNotFoundError(name)

    def find_all(self) -> list[Record]:
        """Retrieves all users in the address book."""
        return self.data

    def add_birthday(self, name: str, birthday: str):
        if not birthday:
            raise ValueError("Provide birthday info.")

        self.find(name).add_birthday(birthday)
        self._persist_data()

    def get_upcoming_birthdays(self):
        """
        Get a list of upcoming birthdays within the next 7 days, including today.

        This function checks the birthdays of users and adjusts the congratulation date
        to the next working day if the birthday falls on a weekend (Saturday or Sunday).

        Returns:
            list: A list of dictionaries containing the user's name and the corresponding
                congratulation date in 'DD.MM.YYYY' format.
        """
        date_format = "%d.%m.%Y"
        today = datetime.today().date()
        upcoming_birthdays = []

        for user in self.data:
            if user.birthday is None:
                continue

            try:
                birthday = datetime.strptime(str(user.birthday), date_format).date()
            except ValueError:
                raise ValueError(
                    f"Incorrect date format for user {user.name}. Expected 'DD.MM.YYYY'."
                )

            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:  # Saturday
                    congratulation_date += timedelta(days=2)  # Move to Monday
                elif congratulation_date.weekday() == 6:  # Sunday
                    congratulation_date += timedelta(days=1)  # Move to Monday

                upcoming_birthdays.append(
                    {
                        "name": user.name,
                        "congratulation_date": congratulation_date.strftime(
                            date_format
                        ),
                    }
                )

        return upcoming_birthdays
