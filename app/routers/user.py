from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut
from app.utils import hash_password

router = APIRouter()


@router.post('/users/', status_code=201, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
	user.password = hash_password(user.password)
	new_user = User(**user.dict())
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user


@router.get('/users/{pk}/', response_model=UserOut)
def get_user(pk: int, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.id == pk).first()
	
	if not user:
		raise HTTPException(status_code=404, detail=f'id {pk} was not found')
	
	return user
