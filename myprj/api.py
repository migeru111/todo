from fastapi import FastAPI
from accessor import DbAccessor
from pydantic import BaseModel
from uuid import UUID
from typing import List

app=FastAPI()

class Todo(BaseModel):
    content:str
    user_id:str

class GetResponse(BaseModel):
    todos:List[Todo|None]

class PostRequestBody(BaseModel):
    content:str

class UpdateRequestBody(BaseModel):
    content:str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/todos",response_model=GetResponse)
async def get_todos(user_id=None):
    accessor=DbAccessor()
    if user_id:
        res=accessor.fetch_by_id(user_id)
    else:
        res=accessor.fetch_all()
    print(res)
    res=[Todo(**i) for i in res]

    return {"todos":res}

@app.post("/todos")
async def post_todos(request_body:PostRequestBody):
    accessor=DbAccessor()
    res=accessor.create(request_body.content)
    return res

@app.put("/todos/{user_id}")
async def put_todos(user_id,request_body:UpdateRequestBody):
    accessor=DbAccessor()
    res=accessor.update(user_id,request_body.content)
    return res

@app.delete("/todos/{user_id}")
async def delete_todos(user_id):
    DbAccessor.delete(user_id=user_id)
    return {"user_id":user_id}    