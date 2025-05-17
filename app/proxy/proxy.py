from fastapi import FastAPI, Request, Response
import os, httpx, json
from openai import OpenAI
from fastapi.responses import JSONResponse,StreamingResponse
from contextlib import asynccontextmanager


NEXTJS = os.getenv("UPSTREAM", "http://localhost:3000")
app    = FastAPI()
Client = httpx.AsyncClient(timeout=None)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO Define all agent here
    app.state.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    app.state.assistant = app.state.client.beta.assistants.create(
    name="Tutor",
    instructions="You are a personal tutor. Write and run code to answer coding questions.",
    model="gpt-4o",
    )
    app.state.thread = app.state.client.beta.threads.create()
    yield
    # optional cleanup on shutdown
    await Client.aclose()

app = FastAPI(lifespan=lifespan)

@app.post("/api/assistants/threads")
async def proxy_return_thread(req: Request):

    return JSONResponse({"threadId": app.state.thread.id})



@app.post("/api/assistants/threads/messages")
async def proxy_messages(req: Request):
    body = await req.json()                       # {'content': 'Paris please!'}
    user_text = body["content"]

    # ---- lightweight transform ---------------------------------
    #TODO ADD instruction here
    developer_text="Add following sentence for every response: Response comes from Python."
    
    new_req  = {"user_content": user_text,
                "developer_content":developer_text,
                "assistantId":app.state.assistant.id}               # SAME SHAPE as browser
    # ------------------------------------------------------------
    
    upstream_url = f"/api/assistants/threads/{app.state.thread.id}/messages"

    resp = await Client.post(upstream_url, json=new_req, stream=True)

    return StreamingResponse(
        resp.aiter_raw(),
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type", "text/event-stream"),
    )
