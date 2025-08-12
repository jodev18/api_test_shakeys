
from fastapi import APIRouter, Depends, HTTPException
from sqlite_db import Regions, session
from user.users import get_current_user
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.exc import IntegrityError

class CreateRegion(BaseModel):
    name: str
    description: Optional[str] = None

class UpdateRegion(BaseModel):
    name: Optional[str] = None

class RegionResponse(BaseModel):
    status: str
    name: str

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

@router.post("/new", response_model=RegionResponse)
async def create_region(region: CreateRegion, current_user: str = Depends(get_current_user)):
    try:
        new_region = Regions(
            region_name=region.name
        )
        session.add(new_region)
        session.commit()
        session.refresh(new_region)
        return RegionResponse(
            status="success",
            name=new_region.region_name
        )
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Region with this name already exists")

@router.put("/{region_id}", response_model=RegionResponse)
async def update_region(region_id: int, region: UpdateRegion, current_user: str = Depends(get_current_user)):
    existing_region = session.query(Regions).filter(Regions.id==region_id).first()
    if not existing_region:
        raise HTTPException(status_code=404, detail="Region not found")
    
    if region.name is not None:
        existing_region.region_name = region.name
    
    session.commit()
    session.refresh(existing_region)
    return RegionResponse(
        status="success",
        name=existing_region.region_name)