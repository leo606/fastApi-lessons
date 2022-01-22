from pyexpat import model
from turtle import title
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

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remove(id, db: Session=Depends(get_db) ):
  blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session= False)
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog {id} not found')
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, req: schemas.Blog, db: Session=Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)

  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f"Blog with id {id} not found")

  blog.update({"title": req.title, "body": req.body })
  db.commit()
  return 'updated'

@app.get('/blog', status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
  blogs = db.query(models.Blog).all()
  return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def byId(id: int, response: Response, db: Session = Depends(get_db)):
  allBlogs = db.query(models.Blog).filter(models.Blog.id == id).first()

  if not allBlogs:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog {id} not found')
  return allBlogs