from typing import Optional

class User:
    def __init__(self, user_id: str, username: str, email: str):
        if "@" not in email:
            raise ValueError("Invalid email format")

        self.user_id = user_id
        self.username = username
        self.email = email
        self.address: Optional[str] = None

    def set_address(self, address: str) -> None:
        if not address or not address.strip():
            raise ValueError("Address cannot be empty")
        self.address = address

    def __repr__(self) -> str:
        return (
            f"User(id={self.user_id}, username={self.username}, "
            f"email={self.email})"
        )
