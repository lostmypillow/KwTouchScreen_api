from pydantic import BaseModel, Field
from typing import Literal
class AuthRequest(BaseModel):
    student_id: str = Field(
        ...,
        pattern=r"^\d{6}$",
        example="300003",
        description="學生學號"
    )
    type: Literal[
        'seats',
        'survey',
        'awards'
    ] = Field(
        ...,
        example="seats",
        description="驗證種類: 補位、評分或獎學金"
    )