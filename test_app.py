import streamlit as st
import requests
import json
import os

from pymongo import MongoClient
from dotenv import load_dotenv
import uuid

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))

db = client["api_testing"]

apis_collection = db["apis"]

# Streamlit Configuration

st.set_page_config(
    page_title="AI API Testing Tool",
    page_icon="🧪",
    layout="wide"
)

st.title("AI-Based API Testing Tool")

# Add API

st.header("Add API")

api_name = st.text_input(
    "API Name",
    placeholder="Example: Create Course"
)

method = st.selectbox(
    "HTTP Method",
    ["GET", "POST", "PUT", "PATCH", "DELETE"]
)

url = st.text_input(
    "API URL",
    placeholder="http://localhost:8000/courses"
)

headers_text = st.text_area(
    "Headers (JSON)",
    value="{}",
    height=100
)

body_text = st.text_area(
    "Request Body (JSON)",
    placeholder='''{
    "string": "string",
    "string": "string"
}''',
    height=150
)
# Save API


if st.button("Save API"):

    if not api_name:
        st.error("Please enter an API name.")

    elif not url:
        st.error("Please enter an API URL.")

    else:

        try:
            headers = json.loads(headers_text)
            body = json.loads(body_text)

            api_data = {
        "id": str(uuid.uuid4()),
        "name": api_name,
        "method": method,
        "url": url,
        "headers": headers,
        "body": body
        }

            apis_collection.insert_one(api_data)

            st.success(f"API '{api_name}' saved successfully.")

        except json.JSONDecodeError:
            st.error("Headers or body contains invalid JSON.")

# Saved APIs


st.header("Saved APIs")

saved_apis = list(
    apis_collection.find()
)

if not saved_apis:

    st.info("No APIs have been saved yet.")

else:

    api_names = [
        api["name"]
        for api in saved_apis
    ]

    selected_name = st.selectbox(
        "Select API",
        api_names
    )

    selected_api = next(
        api for api in saved_apis
        if api["name"] == selected_name
    )

    # Display Selected API

    st.subheader("API Configuration")

    st.write(
        f"**Method:** {selected_api['method']}"
    )

    st.write(
        f"**URL:** {selected_api['url']}"
    )

    st.write("**Headers:**")

    st.json(
        selected_api["headers"]
    )

    st.write("**Body:**")

    st.json(
        selected_api["body"]
    )

    # Execute API
    if st.button("Execute API", type="primary"):

        try:

            response = requests.request(
                method=selected_api["method"],
                url=selected_api["url"],
                headers=selected_api["headers"],
                json=selected_api["body"],
                timeout=30
            )

            # Result

            if response.ok:
                st.success("API Passed")
            else:
                st.error("API Failed")


            st.write(
                f"**Status Code:** {response.status_code}"
            )


            st.subheader("Response")

            try:

                response_json = response.json()

                st.json(response_json)

            except ValueError:

                st.text(response.text)


        except requests.exceptions.RequestException as e:

            st.error(
                f"Request failed: {e}"
            )