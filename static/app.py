################
# Streamlit app
################

import streamlit as st
import requests

st.set_page_config(layout="wide")

# Define the API endpoint URL
API_URL = "https://random-search-service-mn2qfxxd6q-ue.a.run.app/evaluator"

# UI Layout
col1, col2 = st.columns(2)

with col1:
    st.header("Input")
    requirements = st.text_area("Requirements*:", placeholder="Enter job requirements here...")
    uploaded_file = st.file_uploader("Application*:", type=["pdf", "docx", "txt"])

    # Add a message for better guidance
    st.write("*Please provide both the job requirements and the application file.*")

    if st.button("Submit"):
        if uploaded_file is not None and requirements.strip():
            files = {"app_file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"requirements": requirements}
            response = requests.post(API_URL, data=data, files=files)
            
            if response.status_code == 200:
                result = response.json()
                score = result.get("Score")
                strengths = result.get("Strengths")
                areas_for_improvement = result.get("Areas for Improvement")

                with col2:
                    st.header("Response")

                    st.subheader("Score")
                    st.metric(label="Score", value=score)

                    with st.expander("Strengths"):
                        for strength in strengths:
                            st.write(f"- {strength}")

                    with st.expander("Areas for Improvement"):
                        for area in areas_for_improvement:
                            st.write(f"- {area}")

                # Mark the response as shown
                st.session_state.response_shown = True
            else:
                st.error(f"Error: {response.status_code}, {response.text}")

# Only show the initial message if no response has been processed
if "response_shown" not in st.session_state or not st.session_state.response_shown:
    with col2:
        st.header("Response")
        st.write("Submit to see the response here.")
else:
    st.session_state.response_shown = False