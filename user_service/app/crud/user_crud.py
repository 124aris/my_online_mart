from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.user_model import User, UserUpdate

def add_new_user(user_data: User, session: Session):
    user = session.exec(select(User).where(User.email == user_data.email).where(User.name == user_data.name)).one_or_none()
    if user is User:
        raise HTTPException(status_code = 403, detail = "User Already Exists")
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

def get_all_users(session: Session):
    all_users = session.exec(select(User.id, User.name, User.email)).all()
    return all_users

def get_user_by_id(user_id: int, session: Session):
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code = 404, detail = "User Not Found")
    return user

def delete_user_by_id(user_id: int, session: Session):
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code = 404, detail = "User Not Found")
    session.delete(user)
    session.commit()
    return{"message": "User Deleted Successfully"}

def update_user_by_id(user_id: int, to_update_user_data: UserUpdate, session: Session):
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code = 404, detail = "User Not Found")
    hero_data = to_update_user_data.model_dump(exclude_unset = True)
    user.sqlmodel_update(hero_data)
    session.add(user)
    session.commit()
    return user