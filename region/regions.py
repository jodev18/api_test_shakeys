
from fastapi import APIRouter
from sqlite_db import Regions, Provinces, session

router = APIRouter(
    prefix="/regions",
    tags=["Regions"]
)

@router.get("/")
async def list_regions():
    regs = session.query(Regions).all()
    return {
        "data":regs
    }

@router.get("/{region_id}")
async def get_region(region_id: int):
    reg = session.query(Regions).filter(Regions.id==region_id).first()
    return {
        "data":reg
    }