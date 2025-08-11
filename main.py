
from fastapi import FastAPI
from province.provinces import router as prov_router
from region.regions import router as reg_router
from user.users import router as user_router

from data_loader import DataLoader


app = FastAPI()

app.include_router(prov_router)
app.include_router(reg_router)
app.include_router(user_router)

# Load data
dl = DataLoader()
if not dl.check_data():
    dl.load_data()

@app.get("/")
def main_api():
    return{
        "message":"Welcome to Shakeys API"
    }