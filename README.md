# 🤖 AI-Based API Testing & Workflow Agent

An intelligent, full-stack API testing and automation tool that enables developers to interact with and automate REST APIs using natural language commands or an interactive visual workbench.

---

## 🌟 Key Features

- **Natural Language API Automation**: Chat with an autonomous AI agent to create, update, fetch, patch, and delete resources across your API using simple English.
- **Intelligent Error Diagnostics**: Converts raw HTTP errors (400, 401, 404, 422, 500) into plain-English explanations with actionable fix suggestions.
- **Secure Authentication**: Built-in JWT token-based authentication and user registration (`OAuth2PasswordBearer` + `bcrypt`).
- **Interactive Testing Workbench**: Postman-style UI to store API configurations in MongoDB and trigger manual test requests.
- **Hierarchical REST Services**: Pre-built FastAPI endpoints for managing Courses, Modules, and Lessons with full CRUD & partial-update support.

---

## 🛠️ Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
- **AI Agent:** [LangChain](https://www.langchain.com/), [ChatGroq](https://groq.com/) / [Mistral AI](https://mistral.ai/)
- **Database:** [MongoDB](https://www.mongodb.com/) via PyMongo
- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **Security:** JWT (`python-jose` / `PyJWT`), Passlib (`bcrypt`)

---

## 📁 Project Structure

```text
├── app.py            # Streamlit frontend with Login/Register & AI Agent Chat
├── test_app.py       # Streamlit UI for saving and executing manual API tests
├── ai_workflow.py    # LangChain agent with custom REST API tools
├── api_testing.py    # FastAPI service managing Course/Module/Lesson CRUD
├── auth.py           # FastAPI service handling JWT authentication & registration
├── autho.py          # SQLAlchemy user models & token utilities
├── requirements.txt  # Python package dependencies
├── pyproject.toml    # Project metadata and dependencies
├── .env.example      # Example environment configuration template
└── README.md         # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (or Python 3.14 compatible)
- MongoDB instance (local or MongoDB Atlas connection string)
- API Key from [Groq](https://console.groq.com/) or [Mistral AI](https://console.mistral.ai/)

### 2. Clone & Setup Environment

```bash
# Clone the repository
git clone https://github.com/<your-username>/api-based-api-testing-tool.git
cd api-based-api-testing-tool

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to create your `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:
```env
# MongoDB Connection String
MONGODB_URI="mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority"

# LLM API Keys
GROQ_API_KEY="gsk_your_groq_api_key_here"
MISTRAL_API_KEY="your_mistral_api_key_here"
MISTRAL_MODEL="mistral-small-latest"

# Service URLs
API_BASE_URL="http://127.0.0.1:8000"
AUTH_URL="http://localhost:8001"

# JWT Secret
SECRET_KEY="your_generated_secret_key"
```

---

## 🖥️ Running the Application

You will need 3 separate terminal sessions (or run in background):

### 1. Start the REST CRUD API (Port 8000)
```bash
uvicorn api_testing:app --port 8000 --reload
```
Swagger UI docs will be available at: `http://127.0.0.1:8000/docs`

### 2. Start the Authentication Service (Port 8001)
```bash
uvicorn auth:app --port 8001 --reload
```
Auth docs will be available at: `http://localhost:8001/docs`

### 3. Launch the Streamlit Frontend
```bash
streamlit run app.py
```
Or launch the manual testing workbench:
```bash
streamlit run test_app.py
```

---

## 💡 Example Natural Language Prompts

Once logged into the Streamlit AI Assistant (`app.py`), try prompts like:

- *"Create a course named Python with description Basics of Python"*
- *"Add a module named Functions to course <course_id>"*
- *"Get course <course_id>"*
- *"Change only the description of course <course_id> to Advanced concepts"*
- *"Delete course <course_id>"*

The agent will parse your intent, select the appropriate REST method (`POST`, `GET`, `PATCH`, `DELETE`), execute the HTTP call, and return the formatted status and response.

---

## 🔒 Security Notice

Never commit your `.env` file or sensitive credentials to GitHub. Always ensure `.env` is listed in `.gitignore` and use `.env.example` for reference.
