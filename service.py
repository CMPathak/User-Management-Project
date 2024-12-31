from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from utils.emailer import send_email

from schemas import UserCreate, UserUpdate

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    new_result = result.scalars().all()
    return new_result

async def get_user(db: AsyncSession, user_id: int):
    return await db.get(User, user_id)
async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()   
    if not user:
        return None 
    user.name = user_data.name
    user.email = user_data.email
    user.phone = user_data.phone
    user.company = user_data.company
    user.is_active = user_data.is_active 
    await db.commit()
    await db.refresh(user)

    return user 


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    if not db_user:
        return None
    await db.delete(db_user)
    await db.commit()
    return db_user
