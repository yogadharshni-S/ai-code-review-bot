from fastapi import FastAPI, Request
from app.github import handle_pull_request

app=FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request):
    payload=await request.json()
    await handle_pull_request(payload)
    return{"status":"success"}
