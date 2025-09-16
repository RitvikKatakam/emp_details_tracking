from fastapi import FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
import uvicorn

from database import employees_collection
from schemas import EmployeeBase, EmployeeUpdate

app = FastAPI(title="Emp_tracker")

# -------- Create Employee --------
@app.post("/employees", response_model=EmployeeBase)
async def create_employee(employee: EmployeeBase):
    # Ensure employee_id is unique
    existing = await employees_collection.find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID must be unique")

    employee_doc = jsonable_encoder(employee)
    await employees_collection.insert_one(employee_doc)

    # Remove MongoDB’s internal _id before returning
    employee_doc.pop("_id", None)
    return employee_doc


# -------- Get Employee by ID --------
@app.get("/employees/{employee_id}", response_model=EmployeeBase)
async def get_employee(employee_id: str):
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.pop("_id", None)
    return employee


# -------- Update Employee --------
@app.put("/employees/{employee_id}")
async def update_employee(employee_id: str, update: EmployeeUpdate):
    update_data = {k: v for k, v in update.dict(exclude_unset=True).items()}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await employees_collection.update_one(
        {"employee_id": employee_id}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully"}


# -------- Delete Employee --------
@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    result = await employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}


# -------- List Employees --------
@app.get("/employees", response_model=List[EmployeeBase])
async def list_employees(department: Optional[str] = Query(None)):
    query = {"department": department} if department else {}
    cursor = employees_collection.find(query).sort("joining_date", -1)
    employees = await cursor.to_list(length=100)

    for emp in employees:
        emp.pop("_id", None)
    return employees


# -------- Average Salary by Department --------
@app.get("/employees/avg-salary")
async def avg_salary():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"department": "$_id", "avg_salary": 1, "_id": 0}},
    ]
    result = await employees_collection.aggregate(pipeline).to_list(length=100)
    return result


# -------- Search Employees by Skill --------
@app.get("/employees/search", response_model=List[EmployeeBase])
async def search_employees(skill: str):
    cursor = employees_collection.find({"skills": {"$in": [skill]}})
    employees = await cursor.to_list(length=100)

    for emp in employees:
        emp.pop("_id", None)
    return employees


# -------- Main Entry Point --------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
