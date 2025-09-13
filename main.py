# main.py

from fastapi import FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from typing import Optional
from database import employees_collection
from schemas import EmployeeBase, EmployeeUpdate

app = FastAPI()

# 1. Create Employee
@app.post("/employees")
async def create_employee(employee: EmployeeBase):
    if await employees_collection.find_one({"employee_id": employee.employee_id}):
        raise HTTPException(status_code=400, detail="Employee ID must be unique")
    employee_doc = jsonable_encoder(employee)
    await employees_collection.insert_one(employee_doc)
    return employee_doc

# 2. Get Employee by ID
@app.get("/employees/{employee_id}")
async def get_employee(employee_id: str):
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return jsonable_encoder(employee)

# 3. Update Employee (Partial)
@app.put("/employees/{employee_id}")
async def update_employee(employee_id: str, update: EmployeeUpdate):
    update_data = {k: v for k, v in update.dict(exclude_unset=True).items() if v is not None}
    result = await employees_collection.update_one(
        {"employee_id": employee_id}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully"}

# 4. Delete Employee
@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    result = await employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}

# 5. List Employees (by department, sorted)
@app.get("/employees")
async def list_employees(department: Optional[str] = Query(None)):
    query = {}
    if department:
        query["department"] = department
    cursor = employees_collection.find(query).sort("joining_date", -1)
    employees = await cursor.to_list(length=100)
    return jsonable_encoder(employees)

# 6. Average Salary by Department
@app.get("/employees/avg-salary")
async def avg_salary():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"department": "$_id", "avg_salary": 1, "_id": 0}}
    ]
    result = await employees_collection.aggregate(pipeline).to_list(length=100)
    return jsonable_encoder(result)

# 7. Search Employees by Skill
@app.get("/employees/search")
async def search_employees(skill: str):
    cursor = employees_collection.find({"skills": skill})
    employees = await cursor.to_list(length=100)
    return jsonable_encoder(employees)
