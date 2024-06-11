from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from settings import MONGODB_KEY, FRONTEND_URL
from pymongo import MongoClient
from datetime import datetime

from deepface import DeepFace

class Student(BaseModel):
    email: str
    image: str = None
    latitude: str
    longitude: str
    accuracy: str

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins = ['*'], allow_credentials = True, allow_methods = ['*'], allow_headers = ['*'])
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

@app.put('/student')
async def student(data: Student):
    student = db['Student'].find_one({'email': data.email})
    result = DeepFace.verify(
        img1_path = student['image'],
        img2_path = data.image
    )
    if result['verified']:
        return ('Valid')
    else:
        return ('Invalid')
