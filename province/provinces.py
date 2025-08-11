
from fastapi import APIRouter, Depends
from sqlite_db import Regions, Provinces, session
from user.users import get_current_user

router = APIRouter(
    prefix="/provinces",
    tags=["Provinces"]
)

@router.get("/")
async def list_provinces(current_user: str = Depends(get_current_user)):
    provinces = session.query(Provinces).all()
    return {
        "data":provinces
    }

@router.get("/{province_id}")
async def get_province(province_id: int, current_user: str = Depends(get_current_user)):
    provinces = session.query(Provinces).filter(Provinces.id==province_id).first()
    return {
        "data":provinces
    }