from typing import List, Optional

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
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
	posts = db.query(Post).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
	return posts


@router.post('/', status_code=201, response_model=PostOut)
def create_post(post_in: PostCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
	new_post = Post(user_id=user.id, **post_in.dict())
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post


@router.get('/{pk}/', response_model=PostOut)
def get_post(pk: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
	post = db.query(Post).filter(Post.id == pk).one_or_none()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	return post


@router.delete('/{pk}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(pk: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
	qs = db.query(Post).filter(Post.id == pk)
	post = qs.one_or_none()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	if post.user_id != user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'id {pk} is not your post.')
	
	qs.delete(synchronize_session=False)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{pk}/', response_model=PostOut)
def update_post(pk: int, post_in: PostUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
	qs = db.query(Post).filter(Post.id == pk)
	post = qs.one_or_none()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {pk} was not found.')
	if post.user_id != user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'id {pk} is not your post.')
	qs.update(post_in.dict(), synchronize_session=False)
	db.commit()
	return post
