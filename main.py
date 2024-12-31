from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base, engine, get_db
from schemas import UserCreate, UserUpdate, UserResponse
from service import create_user, get_users, get_user, update_user, delete_user
from utils.emailer import send_email
from utils.config import settings
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from models import User
from sqlalchemy.future import select
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

templates = Jinja2Templates(directory="templates")  

app.mount("/static", StaticFiles(directory="static"), name="static")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/addnew", response_class=HTMLResponse)
async def add_new_user_page(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})


@router.get("/edit/{id}", response_class=HTMLResponse)
async def edit_item(id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == id))
    item = result.scalar_one_or_none() 
    if not item:
        return {"error": "Item not found"} 
    return templates.TemplateResponse("edit.html", {"request": request, "item": item})

app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/users", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user(db, user)
    await send_email(new_user.email, "Account Created", "Your account has been created.")
    return new_user

@app.get("/users", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)


@app.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted_user = await delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"} 


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user_details(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
from fastapi import HTTPException


@app.put("/usersupdate/{user_id}")
async def update_user_endpoint(
    user_id: int, 
    user_data: UserUpdate, 
    db: AsyncSession = Depends(get_db)
):
    user = await update_user(user_id, user_data, db) 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")  
    return {"detail": "User updated successfully", "user": user}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)