from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get('/')
def getName():
    return {'data': {'name': 'elvis'}}


@app.get('/blogs')
def getBlogs(limit: int = 10,
             published: bool = True,
             sort: Optional[str] = None):
    if published:
        return {"data": f'{limit} published blogs'}
    return {'data': f'{limit} not published blogs'}


@app.get('/blog/{id}')
def getId(id: int, limit: int = 10):  # is as function param
    return {'param': id, "limit": limit}


# post blog request model:
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def createBlog(req: Blog):
    return {'data': f'blog created with title {req.title}'}
