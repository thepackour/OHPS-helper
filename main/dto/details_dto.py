from dataclasses import dataclass


@dataclass
class DetailsDto:
    main_hand: str
    number_of_keys: str
    multi_input_direction: str
    details: str

    def dict(self):
        return {
            "main_hand": self.main_hand,
            "number_of_keys": self.number_of_keys,
            "multi_input_direction": self.multi_input_direction,
            "details": self.details
        }