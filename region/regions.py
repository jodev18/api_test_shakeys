
from fastapi import APIRouter, Depends
from sqlite_db import Regions, Provinces, session
from user.users import get_current_user

router = APIRouter(
    prefix="/regions",
    tags=["Regions"]
)

@router.get("/")
async def list_regions(current_user: str = Depends(get_current_user)):
    regs = session.query(Regions).all()
    return {
        "data":regs
    }

@router.get("/{region_id}")
async def get_region(region_id: int, current_user: str = Depends(get_current_user)):
    reg = session.query(Regions).filter(Regions.id==region_id).first()
    return {
        "data":reg
    }