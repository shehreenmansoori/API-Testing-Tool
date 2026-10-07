import os
import json
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
#from langchain_mistralai import ChatMistralAI
from langchain_groq import ChatGroq
from langchain.agents import create_agent

load_dotenv()

#MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0.2,api_key=GROQ_API_KEY)

#=============POST===============================
@tool
def create_course(name:str,description:str):
    """Create a course using the course API."""
    response = requests.post( 
        f"{API_BASE_URL}/courses",
    json = {
        "name":name,
        "description":description
    },
    timeout = 30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

@tool
def create_module(course_id:str,name:str):
    """Create a module using the module API."""
    response = requests.post(
        f"{API_BASE_URL}/modules",
        json= {
            "course_id":course_id,
            "name":name
        },
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

@tool
def create_lesson(module_id:str,name:str):
    """Create a lesson using the lesson API."""
    response = requests.post(
        f"{API_BASE_URL}/lesson",
        json={
            "module_id":module_id,
            "name":name
        },
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

#============GET=====================================

@tool
def get_course(course_id:str):
    """Fetch a course using the get course API."""
    response = requests.get(
        f"{API_BASE_URL}/courses/{course_id}",
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

@tool
def get_module(module_id:str):
    """Fetch a module using the get module API."""
    response = requests.get(
        f"{API_BASE_URL}/modules/{module_id}",
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

@tool
def get_lesson(lesson_id:str):
    """Fetch a lesson using the get lesson API."""
    response = requests.get(
        f"{API_BASE_URL}/lesson/{lesson_id}",
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

#=============PUT=======================================
@tool
def update_course(course_id: str, name: str, description: str):
    """Update a course using the course API."""
    response = requests.put(
        f"{API_BASE_URL}/courses/update/{course_id}",
        json={
            "name": name,
            "description": description
        },
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

@tool
def update_module(module_id: str, name: str,course_id:str):
    """Update a module using the module API."""
    response = requests.put(
        f"{API_BASE_URL}/modules/update/{module_id}",
        json={
            "course_id":course_id,
            "name": name,
        },
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

@tool
def update_lesson(module_id: str, name: str,lesson_id:str):
    """Update a lesson using the lesson API."""
    response = requests.put(
        f"{API_BASE_URL}/lesson/update/{lesson_id}",
        json={
            "module_id":module_id,
            "name": name,
        },
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

#============DELETE====================================

@tool
def delete_course(course_id:str):
    """Delete a course using course API"""
    response = requests.delete(
        f"{API_BASE_URL}/courses/delete/{course_id}",
        timeout = 30
    )
    response.raise_for_status()
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

@tool
def delete_module(module_id:str):
    """Delete a module using module API"""
    response = requests.delete(
        f"{API_BASE_URL}/modules/delete/{module_id}",
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }


@tool
def delete_lesson(lesson_id:str):
    """Delete a lesson using lesson API"""
    response = requests.delete(
        f"{API_BASE_URL}/lesson/delete/{lesson_id}",
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }

    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }


#=============PATCH=====================================

@tool
def patch_course(course_id: str, name: str = None, description: str = None):
    """Partially update a course using the course API."""
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    response = requests.patch(
        f"{API_BASE_URL}/courses/patch/{course_id}",
        json=update_data,
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }
    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }
@tool
def patch_module(module_id:str,course_id:str=None,name:str=None):
    """Partially update a module using the module API."""
    update_data={}
    if course_id is not None:
        update_data["course_id"] = course_id
    if name is not None:
        update_data["name"]=name
    response = requests.patch(
        f"{API_BASE_URL}/modules/patch/{module_id}",
        json = update_data,
        timeout=30
    )
    if response.ok:
        return {
            "success": True,
            "status_code": response.status_code,
            "status": response.reason,
            "data": response.json()
        }
    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

@tool
def patch_lesson(lesson_id:str,module_id:str=None,name:str=None):
    """Partially update a lesson using the lesson API."""
    update_data = {}
    if module_id is not None:
        update_data["module_id"]=module_id
    if name is not None:
        update_data["name"]=name
    response = requests.patch(
        f"{API_BASE_URL}/lesson/patch/{lesson_id}",
        json=update_data,
        timeout=30
    )
    if response.ok:
        return {
        "success": True,
        "status_code": response.status_code,
        "status": response.reason,
        "data": response.json()
    }
    return {
        "success": False,
        "status_code": response.status_code,
        "status": response.reason,
        "error": response.text
    }

#=============AGENT=====================================

system_prompt = """
You are an API workflow agent.

You can create and fetch courses, modules and lessons.

Rules:

1. TOOL USAGE
- Always use the available tools to perform operations.
- Never invent IDs.
- Course IDs come from create_course or get_course.
- Module IDs come from create_module or get_module.
- Lesson IDs come from create_lesson or get_lesson.
- When updating or deleting, use the ID provided by the user or returned by a previous tool.

2. UPDATE OPERATIONS
- PUT replaces the complete resource, so collect all required fields before updating.
- PATCH partially updates the resource, so collect only the fields the user wants to change.
- DELETE removes the specified resource.

3. RESPONSE
- Always tell the user which tool was used.
- Always report the HTTP status code when available.
- Clearly state whether the operation succeeded or failed.

4. ERROR EXPLANATION
- Never show raw technical exceptions to the user.
- If an API/tool operation fails, explain what went wrong in simple and human-readable language.
- Use the HTTP status code and error message to determine the likely cause.
- Do not invent a reason that is not supported by the error.
- If the API provides a specific error message, explain that message clearly.

Common HTTP errors:

- 400 Bad Request:
  The request was invalid or required information was missing/incorrect.

- 401 Unauthorized:
  Authentication is missing, invalid, or the user is not authorized.

- 403 Forbidden:
  The request was understood, but the user does not have permission to perform the operation.

- 404 Not Found:
  The requested course, module, or lesson could not be found. The provided ID may not exist.

- 409 Conflict:
  The request conflicts with the current state of the resource, such as trying to create a duplicate resource.

- 422 Unprocessable Entity:
  The request format was understood, but one or more provided values failed validation.

- 500 Internal Server Error:
  Something went wrong on the API server while processing the request.

- For connection errors, timeout errors, or other technical exceptions:
  Explain that the API could not be reached or completed the request and give the user a simple explanation.

5. ERROR RESPONSE FORMAT

When an operation fails, respond using:

Operation: <operation attempted>
Tool used: <exact tool name>
Status: <HTTP status code and status>
What went wrong: <simple explanation of the problem>
Suggested action: <what the user can do to fix it>

Example:

Operation: Fetch course
Tool used: get_course
Status: 404 Not Found
What went wrong: The course with the provided ID could not be found.
Suggested action: Check the course ID and try again.

6. SUCCESS RESPONSE FORMAT

When an operation succeeds, respond using:

Operation: <operation performed>
Tool used: <exact tool name>
Status: <HTTP status code and status>
Result: <short explanation of what happened>

Highlight everything before ":", highlight error code.
"""

agent = create_agent(
    model=llm,
    tools=[
        create_course,
        create_module,
        create_lesson,

        get_course,
        get_module,
        get_lesson,

        update_course,
        update_module,
        update_lesson,

        delete_course,
        delete_module,
        delete_lesson,

        patch_course,
        patch_module,
        patch_lesson
    ],
    system_prompt=system_prompt
)