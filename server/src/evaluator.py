import openai

def feedback(prompt: str) -> str:
    
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
        {"role": "system", "content": """You are an AI assistant designed to evaluate job applications. A user will provide an application and a set of job requirements. Your task is to:
    1. **Analyze the application**: Evaluate the applicant’s qualifications, experience, and skills.
    2. **Compare with the job requirements**: Determine how well the applicant meets the specified job requirements.
    3. **Generate a score**: Provide a score from 0 to 10 indicating the overall fit of the applicant for the job.
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
    """},
        {"role": "user", "content":prompt}
        ],
        max_tokens=500,
        temperature=0.7,
    )

    response = completion.choices[0].message

    return response.content


def evaluate(app_text: str, req_text: str) -> str:

    prompt = f"""
    **Input**:
       - **Application**: {app_text}
       - **Job Requirements**: {req_text}
    Please evaluate and provide a score along with feedback in json object.
    """

    response = feedback(prompt)
    return response