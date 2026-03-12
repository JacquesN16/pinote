from dataclasses import dataclass
from datetime import datetime

@dataclass
class Note:
    id: str
    title: str
    body: str
    created_at: datetime 
    updated_at: datetime 
