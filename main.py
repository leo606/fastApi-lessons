from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
  return {'data': {'name': 'elvis'}}


@app.get('/about')
def about():
  return ['hello, this is about route']