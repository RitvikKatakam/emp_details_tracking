from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class EmployeeBase(BaseModel):
    employee_id: str = Field(..., example="EMP123")
    name: str = Field(..., example="John Doe")
    department: str = Field(..., example="Engineering")
    salary: float = Field(..., example=5000.00)
    joining_date: date = Field(..., example="2023-01-15")
    skills: List[str] = Field(default_factory=list, example=["Python", "Django"])

    class Config:
        orm_mode = True


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Jane Smith")
    department: Optional[str] = Field(None, example="HR")
    salary: Optional[float] = Field(None, example=6000.00)
    joining_date: Optional[date] = Field(None, example="2023-05-10")
    skills: Optional[List[str]] = Field(None, example=["Excel", "Recruitment"])

    class Config:
        orm_mode = True
