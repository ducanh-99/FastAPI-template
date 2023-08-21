from typing import List, Optional

from pydantic import BaseModel


class NewUser(BaseModel):
    user_id: int
    token: str


class NewParent(NewUser):
    student: Optional[List[int]]


class NewTutor(NewUser):
    subject_id: Optional[int]
