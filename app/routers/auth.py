from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserLogin
from app.utils import verify

router = APIRouter(tags=['Authentication'])


@router.post('/login/')
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.email == user_credentials.email).first()
	if not user:
		raise HTTPException(status_code=404, detail='Username and password do not match.')
	if not verify(user_credentials.password, user.password):
		raise HTTPException(status_code=404, detail='Username and password do not match.')
	return {'token': 'token'}
