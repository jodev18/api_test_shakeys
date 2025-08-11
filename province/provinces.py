
from fastapi import APIRouter
from sqlite_db import Regions, Provinces, session

router = APIRouter(
    prefix="/provinces",
    tags=["Provinces"]
)

@router.get("/")
async def list_provinces():
    provinces = session.query(Provinces).all()
    return {
        "data":provinces
    }

@router.get("/{province_id}")
async def get_province(province_id: int):
    provinces = session.query(Provinces).filter(Provinces.id==province_id).first()
    return {
        "data":provinces
    }