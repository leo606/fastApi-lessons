from urllib import response
from fastapi import FastAPI, Depends, Response, status, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(req: schemas.Blog, db: Session = Depends(get_db)):
  new_blog = models.Blog(title = req.title, body = req.body)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog

@app.get('/blog')
def all(db: Session = Depends(get_db)):
  blogs = db.query(models.Blog).all()
  return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def byId(id: int, response: Response, db: Session = Depends(get_db)):
  allBlogs = db.query(models.Blog).filter(models.Blog.id == id).first()

  if not allBlogs:
    response.status_code = status.HTTP_404_NOT_FOUND
    return f'id {id} not found'
  return allBlogs