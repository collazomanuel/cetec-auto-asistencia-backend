from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, timedelta

from deepface import DeepFace
from haversine import haversine, Unit
from uuid import uuid4

from settings import MONGODB_KEY, FRONTEND_URL

class Student(BaseModel):
    email: str
    image: str = None

class Exam(BaseModel):
    code: str
    name: str
    start: str
    length: int
    margin: int

class Attendance(BaseModel):
    email: str
    code: str
    latitude: str
    longitude: str
    accuracy: str
    image: str = None

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins = ['*'], allow_credentials = True, allow_methods = ['*'], allow_headers = ['*'])
client = MongoClient(MONGODB_KEY)
db = client['cetec-auto-asistencia']
building_location = (-34.617639, -58.368056)
building_location_radius = 75
max_accuracy_allowed = 100
date_format = '%Y-%m-%d %H:%M'

@app.get('/exam')
async def exam():
    exams = list(db['Exam'].find({}, {'_id': False}))
    #filtered_exams = list(filter(lambda exam: datetime.now() < (datetime.strptime(exam['start'], date_format) + timedelta(minutes=exam['margin'])), exams))
    filtered_exams = exams
    return (filtered_exams)

@app.post('/exam')
async def exam(data: Exam):
    data.code = uuid4()
    db['Exam'].insert_one(jsonable_encoder(data))
    return ('Ok')

@app.post('/student')
async def student(data: Student):
    db['Student'].insert_one(jsonable_encoder(data))
    return ('Ok')

@app.post('/attendance')
async def attendance(data: Attendance):
    student = db['Student'].find_one({'email': data.email})
    if not validate_location(float(data.latitude), float(data.longitude), float(data.accuracy)):
        return ('Invalid location')
    if not validate_face(student, data.image):
        return ('Invalid face')
    db['Attendance'].insert_one(jsonable_encoder(data))
    return ('Valid')

def validate_location(latitude, longitude, accuracy):
    if accuracy > max_accuracy_allowed:
        return False
    distance = haversine((latitude, longitude), building_location, unit=Unit.METERS)
    if distance - accuracy <= building_location_radius:
        return True
    return False

def validate_face(student, photo):
    #result = DeepFace.verify(img1_path = student['image'], img2_path = photo)
    result = {'verified': True}
    return result['verified'] 
