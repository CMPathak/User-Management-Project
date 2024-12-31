from fastapi import APIRouter,Request, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from typing import Union, Optional
import models



router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/addnew", response_class=HTMLResponse)
async def add(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})