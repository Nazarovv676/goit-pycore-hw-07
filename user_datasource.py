from collections import UserList
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
