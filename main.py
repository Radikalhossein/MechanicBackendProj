from fastapi import FastAPI

from database import Base, engine
from models.services import Car, Company, Service, ServiceItem
from models.users import User
from routers.admin import router as admin_router
from routers.service import router as service_router
from routers.users import router as users_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
Base.metadata.create_all(engine)
app.include_router(users_router, prefix="/user")
app.include_router(admin_router, prefix="/admin")
app.include_router(service_router, prefix="/service")
