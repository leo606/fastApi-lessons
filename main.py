from ast import parse
from ftplib import parse257
from xml.dom.expatbuilder import parseString
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'elvis'}}


@app.get('/blog/{id}')
def get(id: int):  # is as function param
    return {'param': id}
