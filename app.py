from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from chat import chat_conversations
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chatwidget.html", {"request": request})

@app.post("/chatwidget", response_class=HTMLResponse)
async def read_root(request: Request):
    print(request)
    form_data = await request.json()
    query = form_data.get('query')
    response_text = chat_conversations(query)
    return response_text


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

