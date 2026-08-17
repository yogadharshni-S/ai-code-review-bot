import openai
import os

openai.api_key=os.getenv("OPEN_API_KEY")

def review_code(filename,code):
    prompt = f"""
You are a senior software engineer.

Review the code from `{filename}` and provide:
-  Bugs
-  Security issues
-  Performance improvements
-  Code quality suggestions

Respond in bullet points.

Code:
{code}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response["choices"][0]["message"]["content"]