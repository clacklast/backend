from beanie import Document
from typing import Optional
from pydantic import BaseModel

class Movie(Document):
    title: str
    director: Optional[str]
    year: int
    image: Optional[str] = None

    class Settings:
          name = "movies"
    
class MovieUpdate(BaseModel):
    title: Optional[str]
    director: Optional[str]
    year: Optional[int]

class User(Document):
    username: str
    password: str
    
    class Settings:
        name = "users"
