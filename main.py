import os
import requests
import re
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

session = requests.Session()
session.post('https://cloud.mindsdb.com/cloud/login', json={
    'email': os.environ.get("USER_ID"),
    'password': os.environ.get("PASSWORD")
})


app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:8000",
#     "chrome-extension://pgigegiebniooimfefalcnmnkhlndmcb"  # Add your extension's origin
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.post("/chat")
async def chat(request: Request):
    form_data = await request.json()

    input = form_data["question"]
    text = f'"{input}"'

    resp = session.post('https://cloud.mindsdb.com/api/sql/query', json={'query':
        f'SELECT response from mindsdb.gpt_model WHERE author_username = "someuser" AND text = {text};'})
    
    return {'response' : resp.json()["data"][0][0]}



@app.post("/context")
async def summary(request: Request):
    form_data = await request.json()

    input = form_data["question"]
    question = f'"{input}"'

    context = form_data["context"]
    data  = f'"{context}"'

    resp = session.post('https://cloud.mindsdb.com/api/sql/query', json={'query':
                    f'SELECT * FROM que WHERE question = {question} AND text = {data} ;'})

    return (resp.json()["data"][0][0])



@app.post("/image")
async def image(request: Request):
    form_data = await request.json()

    base = form_data["base"]
    input = f'"{base}"'

    # extra = form_data["extra"]
    # output = f'"{extra}"'

    resp = session.post('https://cloud.mindsdb.com/api/sql/query', json={'query':
                    f'SELECT response from mindsdb.gpt_image_3 WHERE input = {input};'})
    
    return (resp.json()["data"][0][0])


@app.post("/web")
async def summary(request: Request):
    form_data = await request.json()

    input = form_data["question"]
    question = f'"{input}"'

    context = form_data["context"]
    url  = f'"{context}"'

    # url = '"https://docs.mindsdb.com/what-is-mindsdb"'
    resp_4 = session.post('https://cloud.mindsdb.com/api/sql/query', json={'query':
                    f'SELECT text_content FROM my_web.crawler WHERE url = {url} LIMIT 1;'})

    s = (resp_4.json()["data"][0][0])
    a = re.sub(r"\s+", "", s)
    b = a[:1500]

    print("**"*10)
    print(b)
    # question = '"what is mindsdb"'
    data = f'"{b}"'

    resp_5 = session.post('https://cloud.mindsdb.com/api/sql/query', json={'query':
                        f'SELECT * FROM que WHERE question = {question} AND text = {data} ;'})


    print(resp_5.json()["data"][0][0])

    return (resp_5.json()["data"][0][0])


