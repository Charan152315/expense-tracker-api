from fastapi import APIRouter,HTTPException,status,Depends
from passlib.context import CryptContext
from .. import models,schemas,utils,database,auth
from sqlalchemy.orm import Session 
from .. database import get_db

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print("Received user data:", user.dict())
    try:
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Email was already registered"
            )

        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password

        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print("New user created successfully:", new_user.email)
        return new_user

    except Exception as e:
        import traceback
        print(" Error in /users/ route:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/",response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db),
                  current_user: models.User = Depends(auth.get_current_user)):
    users = db.query(models.User).all()
    return users


@router.put("/set_limit")
def set_monthly_limit(limit:float,db:Session=Depends(database.get_db),
    current_user:models.User=Depends(auth.get_current_user)):

    if limit<=0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Limit must be greater than zero")
    
    current_user.monthly_limit=limit
    db.commit()
    db.refresh(current_user)
    return{"message":f"monthly limit set to {limit}"}
