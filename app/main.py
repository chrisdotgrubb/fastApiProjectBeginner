from fastapi import FastAPI, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from .models import PostIn, Post, Base
from .database import engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/posts/')
def get_posts(db: Session = Depends(get_db)):
	posts = db.query(Post).all()
	context = {
		'data': {'posts': posts}
	}
	return context


@app.post('/posts/', status_code=201)
def create_post(post: PostIn, db: Session = Depends(get_db)):
	new_post = Post(**post.dict())
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	context = {
		'data': {'post': new_post}
	}
	return context


@app.get('/posts/{pk}/')
def get_post(pk: int, db: Session = Depends(get_db)):
	post = db.query(Post).filter(Post.id == pk).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	context = {
		'data': {'post': post}
	}
	return context


@app.delete('/posts/{pk}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(pk: int, db: Session = Depends(get_db)):
	post = db.query(Post).filter(Post.id == pk)
	if not post.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	post.delete(synchronize_session=False)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{pk}/')
def update_post(pk: int, post: PostIn, db: Session = Depends(get_db)):
	qs = db.query(Post).filter(Post.id == pk)
	
	if not qs.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	qs.update(post.dict(), synchronize_session=False)
	db.commit()
	return {'data': {'post': qs.first()}}
