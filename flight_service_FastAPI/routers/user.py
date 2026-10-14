from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse,UpdateUser
from services.user import create_user as create_user_service, delete_user, update_user, all_users, user_by_id

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user_service(db, user)




@router.get("/",response_model = list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db)
):
   return all_users(db)



@router.get("/{userId}" , response_model = UserResponse)

def get_user_by_id(
    userId : int,
    db : Session = Depends(get_db)
):

    return user_by_id(db, userId)




@router.put("/{userId}" , response_model= UpdateUser)
def Update_user(
    userId : int,
    updated_user : UpdateUser,
    db : Session = Depends(get_db)
):
    return update_user(db, userId, updated_user)



@router.delete("/{userId}")
def del_user(
    userId : int,
    db : Session = Depends(get_db)
):
    return delete_user(db, userId) 