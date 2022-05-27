from typing import List

from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post
from app.oauth2 import get_current_user
from app.schemas import PostCreate, PostUpdate, PostOut

router = APIRouter(
	prefix='/posts',
	tags=['posts', ]
)


@router.get('/', response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
	posts = db.query(Post).all()
	return posts


@router.post('/', status_code=201, response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
	new_post = Post(**post.dict())
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post


@router.get('/{pk}/', response_model=PostOut)
def get_post(pk: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
	post = db.query(Post).filter(Post.id == pk).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	return post


@router.delete('/{pk}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(pk: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
	post = db.query(Post).filter(Post.id == pk)
	if not post.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	post.delete(synchronize_session=False)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{pk}/', response_model=PostOut)
def update_post(pk: int, post: PostUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
	qs = db.query(Post).filter(Post.id == pk)
	
	if not qs.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	qs.update(post.dict(), synchronize_session=False)
	db.commit()
	return qs.first()
