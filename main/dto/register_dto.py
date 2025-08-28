from dataclasses import dataclass


@dataclass
class RegisterDto:
    id: str
    username: str

    def dict(self):
        return {
            "id": self.id,
            "username": self.username
        }