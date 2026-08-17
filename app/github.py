import requests
import os
from app.ai_reviewer import review_code

GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")

HEADERS={
    "Authorization":f"token {GITHUB_TOKEN}",
    "Accept":"application/vnd.github.v3+json"
}

async def handle_pull_request(payload):

    if payload.get("action") not in ["opened","synchronize"]:
        return
    
    pr=payload["pull_request"]
    repo=payload["repository"]["full_name"]
    pr_number=pr["number"]

    files_url=pr["url"] + "/files"
    files=requests.get(files_url, headers=HEADERS).json()

    review_comments=[]

    for file in files:
        if"patch" in file:
            feedback=review_code(file["filename"], file["patch"])
            review_comments.appen(
                f"### {file['filename']}\n{feedback}"
            )

    if review_comments:
        post_comment(repo, pr_number, "\n\n".join(review_comments))

def post_comment(repo,pr_number,body):
    url=f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    requests.post(url,headers=HEADERS, json={"body":body})
