from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from settings import MONGODB_KEY, FRONTEND_URL
from pymongo import MongoClient
from datetime import datetime

from deepface import DeepFace

from haversine import haversine, Unit

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
building_location = (-34.617639, -58.368056)
building_location_radius = 75
max_accuracy_allowed = 100

@app.post('/student')
async def student(data: Student):
    db['Student'].insert_one(jsonable_encoder({
        'image': data.image,
        'email': data.email,
        'latitude': data.latitude,
        'longitude': data.longitude,
        'accuracy': data.accuracy,
        'date': datetime.now()
    }))
    return ('Ok')

@app.put('/student')
async def student(data: Student):
    if not validate_location(float(data.latitude), float(data.longitude), float(data.accuracy)):
        return ('Invalid location')
    #student = db['Student'].find_one({'email': data.email})
    #result = DeepFace.verify(img1_path = student['image'], img2_path = data.image)
    result = {'verified': True}
    if result['verified']:
        return ('Valid')
    else:
        return ('Invalid face')

def validate_location(latitude, longitude, accuracy):
    if accuracy > max_accuracy_allowed:
        return False
    accuracy = 0
    distance = haversine((latitude, longitude), building_location, unit=Unit.METERS)
    if (distance - accuracy) <= building_location_radius:
        return True
    return False
