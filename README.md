# random-search-application-scoring-system
Application Scoring MVP for Random Search

### Steps to interact with the application and endpoints 
----
1. FastAPI Endpoints: 
```
https://random-search-service-mn2qfxxd6q-ue.a.run.app
# visit https://random-search-service-mn2qfxxd6q-ue.a.run.app/docs and Tryout the POST method /evaluator
```
2. Webapp (https://github.com/Krishna2709/random-search-application-scoring-system/static/)): 
```
https://application-scoring.streamlit.app
```

# Project Overview *(v1)*
- **Technology Stack**:
  ```
    - Docker (Dockerfile is defined to create a docker image for deployment)
  
    - FastAPI (to create and expose the endpoints)

    - Google Cloud Run (server to deploy the FastAPI endpoints)
  
    - OpenAI (for LLMs)

    - Python (programming language)
  
    - Streamlit (for front-end)
  ```

### Prompts
- **System Prompt**:
  ```
  You are an AI assistant designed to evaluate job applications. A user will provide an application and a set of job requirements. Your task is to:

    1. **Analyze the application**: Evaluate the applicant's qualifications, experience, and skills.
    2. **Compare with the job requirements**: Determine how well the applicant meets the specified job requirements.
    3. **Generate a score**: Provide a score from 0 to 10, indicating the overall fit of the applicant for the job.
    4. **Provide feedback**: Offer constructive feedback, highlighting the applicant's strengths and areas for improvement.
    Respond in the following JSON format:
        "Score": <numerical score from 0 to 10>,
        "Strengths": [
            "Strength 1",
            "Strength 2",
            ...
        ],
        "Areas for Improvement": [
            "Improvement 1",
            "Improvement 2",
            ...
        ]
  ```
- **User Prompt**:
  ```
  """
    **Input**:
       - **Application**: {app_text}
       - **Job Requirements**: {req_text}
    Please evaluate and provide a score along with feedback in the JSON object.
  """
  ```
### Features
----
- Defined Pydantic Validators for Input Validation
- FastAPI endpoint is deployed on Cloud Run with 2 instances to mitigate cold start
- Simple Streamlit web app for UX
- OpenAI gpt-3.5-turbo for better and faster responses.
  
### Further Improvements
----

- CI/CD pipeline using GitHub Actions & Cloud Run
- Store the inputs and responses to support history and caching
- The stored info can be loaded into PSQL db for the caching mechanism
- Validate Requirements content to mitigate potential misuse
- Check the uploaded file for malicious content like prompt injection
- Use open-source LLMs for cost reduction
- Utilize Ray from Anyscale for scaling
- Implement the Shadow model mechanism to evaluate responses from different LLMs.
- Multilingual Support
- ...
- ...

