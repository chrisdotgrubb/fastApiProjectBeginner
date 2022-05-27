from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.oauth2 import create_access_token
from app.database import get_db
from app.models import User
from app.schemas import UserLogin, Token
from app.utils import verify

router = APIRouter(tags=['Authentication'])


@router.post('/login/', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = db.query(User).filter(User.email == user_credentials.username).first()
	if not user:
		raise HTTPException(status_code=403, detail='Username and password do not match.')
	if not verify(user_credentials.password, user.password):
		raise HTTPException(status_code=403, detail='Username and password do not match.')
	token = create_access_token(data={'user_id': user.id})
	return {'token': token, 'token_type': 'bearer'}
