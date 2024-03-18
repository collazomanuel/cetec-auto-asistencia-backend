from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from settings import MONGODB_KEY, BACKEND_URL
from pymongo import MongoClient
from datetime import datetime

class Student(BaseModel):
    email: str
    image: str = None
    latitude: str
    longitude: str
    accuracy: str

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins = [BACKEND_URL], allow_credentials = True, allow_methods = ['*'], allow_headers = ['*'])
client = MongoClient(MONGODB_KEY)
db = client['cetec-auto-asistencia']

@app.post('/student')
async def student(data: Student):
    db['Student'].insert_one(jsonable_encoder({
        'image': data.image,
        'email': data.email,
        'latitude': data.latitude,
        'longitude': data.longitude,
        'accuracy': data.accuracy,
        'date': datetime.utcnow()
    }))
    return ('Ok')
