
from pydantic import BaseModel, Field
from typing import Literal


class RateableEmployee(BaseModel):
    學號: str = Field(
        ...,
        example="000000",
        pattern=r"^\d{6}$",
        description="員工編號"
    )
    姓名: str = Field(
        ...,
        example="王小明",
        description="就...姓名"
    )
    主要部門: Literal["導師組", "招生部", "櫃台", "數輔", "補課教室"] = Field(
        ...,
        example="櫃台",
        description="部門"
    )
