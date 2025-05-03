from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.crud.crud_user import get_user_by_email, create_user
from app.schemas.user import UserCreate, UserOut, Token
from app.core.security import verify_password, create_access_token

router = APIRouter(
    tags=["Authentication"],
    responses={401: {"description": "Unauthorized"}}
)

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return create_user(db, user_in)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(current_user=Depends(get_current_user)):
    """
    JWT logout is typically handled client-side by discarding the token.
    Implement a token blacklist here if you need server-side invalidation.
    """
    return {"msg": "Logout successful"}
