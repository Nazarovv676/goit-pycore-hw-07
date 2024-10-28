from functools import wraps
from address_book import DatabaseNotFoundError, UserNotFoundError


def input_error(error_message="🤖\tProvide all required parameters please."):
    """
    A decorator that handles common input-related errors.

    Parameters:
        error_message (str): The message to return when a ValueError occurs.

    Returns:
        function: The decorated function with error handling.
    """

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return error_message  # Return the provided error message for ValueError
            except DatabaseNotFoundError:
                return "🤖\tDatabase not found."  # Handle database not found error
            except UserNotFoundError as e:
                return (
                    f"🤖\t{e}"  # Return a user-friendly message for UserNotFoundError
                )

        return inner

    return decorator
