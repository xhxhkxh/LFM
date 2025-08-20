"""Simple data models used by views."""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Post:
    id: int
    title: str
    content: str
    author: str
    ptime: str
    aid: int
    aem: Optional[str] = None
    commentL: List = field(default_factory=list)


@dataclass
class Reply:
    content: str
    aid: Optional[int]
    authorName: str
    authorEmail: Optional[str]

    def __str__(self):
        return f"{self.content} by {self.authorName} ({self.aid})"
