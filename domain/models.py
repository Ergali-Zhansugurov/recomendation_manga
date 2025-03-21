from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Manga:
    id: int
    format: str = ""
    status: str = ""
    start_date: Dict[str, Any] = field(default_factory=dict)
    average_score: int = 0
    mean_score: int = 0
    popularity: int = 0
    favourites: int = 0
    source: str = ""
    genres: List[str] = field(default_factory=list)
    title: Dict[str, str] = field(default_factory=dict)
    synonyms: List[str] = field(default_factory=list)
    tags: List[Dict[str, Any]] = field(default_factory=list)
    cover_image: Dict[str, str] = field(default_factory=dict)
    characters: List[Dict[str, Any]] = field(default_factory=list)
    reviews: Dict[str, Any] = field(default_factory=dict)