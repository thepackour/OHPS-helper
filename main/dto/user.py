from dataclasses import dataclass


@dataclass
class User:
    id: str
    last_level_clear: int
    last_quest_clear: int
    username: str
    level: int
    exp: int
    tier: int
    main_hand: str
    number_of_keys: str
    multi_input_direction: str
    details: str
    created_at: str
    deleted_at: str