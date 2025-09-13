from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class EmployeeBase(BaseModel):
    employee_id: str = Field(..., description="Unique employee identifier")
    name: str = Field(..., min_length=1, description="Employee name")
    department: str = Field(..., min_length=1, description="Department name")
    salary: float = Field(..., gt=0, description="Employee salary")
    joining_date: str = Field(..., description="Joining date (YYYY-MM-DD format)")
    skills: List[str] = Field(..., min_items=1, description="List of skills")

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "E123",
                "name": "John Doe",
                "department": "Engineering",
                "salary": 75000,
                "joining_date": "2023-01-15",
                "skills": ["Python", "MongoDB", "APIs"]
            }
        }

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    department: Optional[str] = Field(None, min_length=1)
    salary: Optional[float] = Field(None, gt=0)
    joining_date: Optional[str] = None
    skills: Optional[List[str]] = Field(None, min_items=1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Smith",
                "salary": 80000,
                "skills": ["Python", "FastAPI", "Docker"]
            }
        }