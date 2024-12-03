from bson import ObjectId
from fastapi import APIRouter, status ,HTTPException
from database import *
from models import * 

student_router = APIRouter()

# To insert a new student
@student_router.get('/')
def std():
    return ({"msg":"welcome"})


@student_router.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    student_dict = student.dict()
    result = collection.insert_one(student_dict)
    return {"id": str(result.inserted_id)}


@student_router.get("/students",status_code=status.HTTP_201_CREATED)
def list_students(country: str = None, age: int = None):
    query = dict()
    if country:
        query["country"] = country
    if age:
        query['age']={'$gte':age}
    students = collection.find(query,{'name':1,'age':1,'_id':0})
    return {"data": [student for student in students]}



@student_router.get('/students/{id}',status_code=status.HTTP_200_OK)
def find_student(id:str):
    std=collection.find_one({'_id':ObjectId(id)}, {'_id':0})
    if not std:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    return std


@student_router.patch('/students/{id}',status_code=status.HTTP_204_NO_CONTENT)
def update_student(id:str,updated_info:StudentUpdate):
    id=ObjectId(id)
    updated_info=updated_info.model_dump(exclude_unset=True)
    if not updated_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    
    result=collection.update_one({'_id':id},{'$set':updated_info})

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")



@student_router.delete('/students/{id}',status_code=status.HTTP_200_OK)
def delete_student(id:str):
    id=ObjectId(id)
    result=collection.delete_one({'_id':id})
    if  result.deleted_count ==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return {"message": "Student deleted successfully"}   

