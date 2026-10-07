import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import uuid
from typing import Optional
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["api_testing"]
apis_collection = db["apis"]


class Course(BaseModel):
    name: str
    description: str


class Module(BaseModel):
    course_id: str
    name: str


class Lesson(BaseModel):
    module_id: str
    name: str

#FOR PATCH ONLY
class CoursePatch(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ModulePatch(BaseModel):
    course_id: Optional[str] = None
    name: Optional[str] = None


class LessonPatch(BaseModel):
    module_id: Optional[str] = None
    name: Optional[str] = None

#============================POST==============================================

@app.post("/courses")
async def create_course(course: Course):
    course_id = str(uuid.uuid4())
    course_data = {
        "id": course_id,
        "name": course.name,
        "description": course.description,
        "status": "draft"
    }
    apis_collection.insert_one(course_data)
    course_data.pop("_id", None)
    return course_data


@app.post("/modules")
async def create_module(module: Module):
    module_id = str(uuid.uuid4())
    module_data = {
        "id": module_id,
        "course_id":module.course_id,
        "name":module.name
    }
    apis_collection.insert_one(module_data)
    module_data.pop("_id", None)
    return module_data


@app.post("/lesson")
async def create_lesson(lesson: Lesson):
    lesson_id = str(uuid.uuid4())
    lesson_data = {
        "id": lesson_id,
        "module_id":lesson.module_id,
        "name":lesson.name
    }
    apis_collection.insert_one(lesson_data)
    lesson_data.pop("_id", None)
    return lesson_data


# @app.post("/courses/{course_id}/publish")
# async def publish_course(course_id: int):
#     return {
#         "course_id": course_id,
#         "status": "published"
#     }



#============================GET==============================================

@app.get("/courses/{course_id}")
async def get_course(course_id: str):
    course = apis_collection.find_one(
        {
            "id": course_id,
            "name": {"$exists": True},
            "description": {"$exists": True}
        },
        {"_id": 0}
    )
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    return course


@app.get("/modules/{module_id}")
async def get_module(module_id: str):
    module = apis_collection.find_one(
        {
            "id": module_id,
            "course_id": {"$exists": True},
            "name": {"$exists": True}
        },
        {"_id": 0}
    )
    if not module:
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )
    return module

@app.get("/lesson/{lesson_id}")
async def get_lesson(lesson_id: str):
    lesson = apis_collection.find_one(
        {
            "id": lesson_id,
            "module_id": {"$exists": True},
            "name": {"$exists": True}
        },
        {"_id": 0}
    )
    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )
    return lesson


#============================DELETE==============================================

@app.delete("/courses/delete/{course_id}")
async def delete_course(course_id: str):
    course = apis_collection.find_one(
        {
            "id": course_id,
            "name": {"$exists": True},
            "description": {"$exists": True}
        })
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    apis_collection.delete_one(
        {
            "id": course_id,
            "name": {"$exists": True},
            "description": {"$exists": True}
        })
    return {
            "message": "Course deleted successfully",
            "id": course_id
        }


@app.delete("/modules/delete/{module_id}")
async def delete_module(module_id: str):
    module = apis_collection.find_one({
        "id": module_id,
        "course_id": {"$exists": True},
        "name": {"$exists": True}
    })
    if not module:
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )
    apis_collection.delete_one({
        "id": module_id,
        "course_id": {"$exists": True},
        "name": {"$exists": True}
    })
    return {
        "message": "Module deleted successfully",
        "id": module_id
    }


@app.delete("/lesson/delete/{lesson_id}")
async def delete_lesson(lesson_id: str):
    lesson = apis_collection.find_one(
            {
                "id": lesson_id,
                "module_id": {"$exists": True},
                "name": {"$exists": True}
            })
    if not lesson:
        raise HTTPException(
                status_code=404,
                detail="Lesson not found"
            )
    apis_collection.delete_one(
        {
            "id": lesson_id,
            "module_id": {"$exists": True},
            "name": {"$exists": True}
        })
    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )
    return {
            "message": "Lesson deleted successfully",
            "id": lesson_id
        }


#============================PUT==============================================

@app.put("/courses/update/{course_id}")
async def update_course(course_id: str, course: Course):
    existing_course = apis_collection.find_one({
        "id": course_id,
        "name": {"$exists": True},
        "description": {"$exists": True}
    })
    if not existing_course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    apis_collection.update_one(
        {"id": course_id},
        {
            "$set": {
                "name": course.name,
                "description": course.description
            }
        }
    )
    updated_course = apis_collection.find_one(
        {"id": course_id},
        {"_id": 0}
    )
    return updated_course



@app.put("/modules/update/{module_id}")
async def update_module(module_id: str, module: Module):
    existing_module = apis_collection.find_one({
        "id": module_id,
        "course_id": {"$exists": True},
        "name": {"$exists": True}
    })
    if not existing_module:
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )
    apis_collection.update_one(
        {"id": module_id},
        {
            "$set": {
                "course_id": module.course_id,
                "name": module.name
            }
        }
    )
    updated_module = apis_collection.find_one(
        {"id": module_id},
        {"_id": 0}
    )
    return updated_module



@app.put("/lesson/update/{lesson_id}")
async def update_lesson(lesson_id: str, lesson: Lesson):
    existing_lesson = apis_collection.find_one({
        "id": lesson_id,
        "module_id": {"$exists": True},
        "name": {"$exists": True}
    })
    if not existing_lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )
    apis_collection.update_one(
        {"id": lesson_id},
        {
            "$set": {
                "module_id": lesson.module_id,
                "name": lesson.name
            }
        }
    )
    updated_lesson = apis_collection.find_one(
        {"id": lesson_id},
        {"_id": 0}
    )
    return updated_lesson

#============================PATCH==============================================

@app.patch("/courses/patch/{course_id}")
async def patch_course(course_id: str, course: CoursePatch):
    existing_course = apis_collection.find_one({
        "id": course_id,
        "description": {"$exists": True}
    })
    if not existing_course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    update_data = course.model_dump(exclude_unset=True) #will exclude a field if user didnt change it

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields to update"
        )
    
    apis_collection.update_one(
        {"id": course_id},
        {"$set": update_data}
    )
    updated_course = apis_collection.find_one(
        {"id": course_id},
        {"_id": 0} #exclue mongodb objectid
    )
    return updated_course


@app.patch("/modules/patch/{module_id}")
async def patch_module(module_id: str, module: ModulePatch):
    existing_module = apis_collection.find_one({
        "id": module_id,
        "course_id": {"$exists": True},
        "name": {"$exists": True}
    })
    if not existing_module:
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )
    update_data = module.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields to update"
        )
    
    apis_collection.update_one(
        {"id": module_id},
        {"$set": update_data}
    )
    updated_module = apis_collection.find_one(
        {"id": module_id},
        {"_id": 0}
    )
    return updated_module

@app.patch("/lesson/patch/{lesson_id}")
async def patch_lesson(lesson_id: str, lesson: LessonPatch):
    existing_lesson = apis_collection.find_one({
        "id": lesson_id,
        "module_id": {"$exists": True},
        "name": {"$exists": True}
    })
    if not existing_lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )
    update_data = lesson.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields to update"
        )

    apis_collection.update_one(
        {"id": lesson_id},
        {"$set": update_data}
    )
    updated_lesson = apis_collection.find_one(
        {"id": lesson_id},
        {"_id": 0}
    )
    return updated_lesson