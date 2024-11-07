from pydantic import BaseModel
from typing import Optional

class Note(BaseModel):
    id: str
    title: str
    desc: str
    important: Optional[bool]=False
    image: Optional[str] 