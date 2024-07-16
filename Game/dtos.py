from dataclasses import dataclass, field


@dataclass
class CharTypeDTO:
    name: str
    difficulty: int = 0
    bonus: list[str] = field(default_factory=lambda: list())
    provision: float = 0


@dataclass
class PlayerDTO:
    sex: str
    age: int
    sick: CharTypeDTO
    hobby: CharTypeDTO
    phobia: CharTypeDTO
    baggage: CharTypeDTO
    quality: CharTypeDTO
    knowledge: CharTypeDTO
    job: CharTypeDTO


@dataclass
class BunkerDTO:
    catastrophe: str
    season: str
    season_type: str
    location: str
    rooms: str
    places: int
    time: int
    timeout: int
    food: int
    skill_data: dict[str, int]
    win_req: int


@dataclass
class GameDTO:
    info: BunkerDTO
    players: list[PlayerDTO]
