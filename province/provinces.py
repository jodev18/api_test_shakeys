from fastapi import APIRouter, Depends, HTTPException
from sqlite_db import Regions, Provinces, session
from user.users import get_current_user
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.exc import IntegrityError

class CreateProvince(BaseModel):
    name: str
    region_id: int

class UpdateProvince(BaseModel):
    name: Optional[str] = None
    region_id: Optional[int] = None

class ProvinceResponse(BaseModel):
    name: str
    region_id: int

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

@router.post("/new", response_model=ProvinceResponse)
async def create_province(province: CreateProvince, current_user: str = Depends(get_current_user)):
    try:
        new_province = Provinces(
            province_name=province.name,
            region_id=province.region_id
        )
        session.add(new_province)
        session.commit()
        session.refresh(new_province)
        return ProvinceResponse(
            name=new_province.province_name,
            region_id=new_province.region_id
        )
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Province with this name or region already exists.") 

@router.put("/{province_id}", response_model=ProvinceResponse)
async def update_province(province_id: int, province: UpdateProvince, current_user: str = Depends(get_current_user)):
    existing_province = session.query(Provinces).filter(Provinces.id==province_id).first()
    if not existing_province:
        raise HTTPException(status_code=404, detail="Province not found")  # Changed to proper HTTP exception
    
    try:
        if province.name:
            existing_province.province_name = province.name  # Make sure this matches your DB column name
        if province.region_id is not None:
            existing_region = session.query(Regions).filter(Regions.id == province.region_id).first()
            if not existing_region:
                raise HTTPException(status_code=404, detail="Region not found")
            existing_province.region_id = province.region_id
        
        session.commit()
        session.refresh(existing_province)
        
        return ProvinceResponse(
            name=existing_province.province_name,
            region_id=existing_province.region_id
        )
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Update failed due to database constraints")