from fastapi import FastAPI
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio
from dotenv import load_dotenv

load_dotenv(".env")
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(request: Request):
    chat_in = await request.json()
    user_content = chat_in.get('content')
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant.Follow the user's instructions carefully. Respond using markdown."},
            {"role": "user", "content": user_content},
        ],
    )
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)