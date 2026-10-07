import importlib.util
from pathlib import Path
import requests
import os

import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI API Workflow Agent",
    page_icon="🤖",
    layout="centered",
)


# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8001")


def login_page():
    st.title("AI API Workflow Agent")
    st.subheader("Welcome back")

    st.write("Login to access the application.")

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login", use_container_width=True):

        if not username or not password:
            st.error("Please enter your username and password.")
            return

        try:
            response = requests.post(
                f"{AUTH_URL}/token",
                data={
                    "username": username,
                    "password": password,
                },
            )

            if response.status_code == 200:

                token_data = response.json()

                st.session_state["access_token"] = token_data["access_token"]
                st.session_state["username"] = username
                st.session_state["logged_in"] = True

                st.rerun()

            else:
                try:
                    error_detail = response.json().get(
                        "detail",
                        "Incorrect username or password."
                    )
                except Exception:
                    error_detail = "Incorrect username or password."

                st.error(error_detail)

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the authentication server. "
                "Make sure FastAPI is running."
            )


def register_page():
    st.title("AI API Workflow Agent")
    st.subheader("Create an account")

    st.write("Register a new account to use the application.")

    username = st.text_input(
        "Username",
        key="register_username"
    )

    email = st.text_input(
        "Email",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="register_confirm_password"
    )

    if st.button("Create Account", use_container_width=True):

        if not username or not email or not password:
            st.error("Please fill in all fields.")
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        try:
            response = requests.post(
                f"{AUTH_URL}/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                },
            )

            if response.status_code == 200:

                st.success(
                    "Account created successfully! "
                    "You can now login."
                )

            else:
                try:
                    error_detail = response.json().get(
                        "detail",
                        "Registration failed."
                    )
                except Exception:
                    error_detail = "Registration failed."

                st.error(error_detail)

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the authentication server. "
                "Make sure FastAPI is running."
            )


# --------------------------------------------------
# LOGIN / REGISTER SCREEN
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


if not st.session_state["logged_in"]:

    tab1, tab2 = st.tabs(
        ["Login", "Create Account"]
    )

    with tab1:
        login_page()

    with tab2:
        register_page()

    st.stop()


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

st.title("AI API Workflow Agent")

st.caption(
    "Create, fetch, update, partially update, and delete "
    "courses, modules, and lessons using natural language."
)


# --------------------------------------------------
# LOAD AI WORKFLOW
# --------------------------------------------------

workflow_path = Path(__file__).with_name("ai_workflow.py")

spec = importlib.util.spec_from_file_location(
    "ai_workflow",
    workflow_path,
)

workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)

agent = workflow.agent


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("Examples")

    st.write("Try requests like:")

    st.code(
        "Create a course named Python with description Basics of Python"
    )

    st.code("Get course 123")

    st.code(
        "Update course 123 with name Advanced Python and description Deep dive"
    )

    st.code(
        "Change only the description of course 123 to Advanced concepts"
    )

    st.code("Delete course 123")

    st.divider()

    st.write(
        f"Logged in as: **{st.session_state['username']}**"
    )

    if st.button("Logout", use_container_width=True):

        st.session_state["logged_in"] = False
        st.session_state.pop("access_token", None)
        st.session_state.pop("username", None)
        st.session_state.messages = []

        st.rerun()

    if st.button("Clear chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "What would you like to do?"
)


if user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Working..."):

            try:

                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": message["role"],
                                "content": message["content"],
                            }
                            for message in st.session_state.messages
                        ]
                    }
                )

                response = result["messages"][-1].content

                # Handle structured responses
                if isinstance(response, list):

                    response = "\n".join(
                        item.get("text", str(item))
                        if isinstance(item, dict)
                        else str(item)
                        for item in response
                    )

                st.write(response)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )

            except Exception as e:

                error_message = f"Error: {e}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )