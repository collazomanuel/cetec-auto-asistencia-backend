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
    latitude: float
    longitude: float
    accuracy: float
    image: str = None

building_location = (-34.617639, -58.368056)
building_location_radius = 150
max_accuracy_allowed = 100
date_format = '%Y-%m-%d %H:%M'

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins = [FRONTEND_URL], allow_credentials = True, allow_methods = ['*'], allow_headers = ['*'])
client = MongoClient(MONGODB_KEY)
db = client['cetec-auto-asistencia']

@app.get('/exam')
async def exam():
    exams = list(db['Exam'].find({}, {'_id': False}))
    filtered_exams = list(filter(lambda exam: datetime.now() < (datetime.strptime(exam['start'], date_format) + timedelta(minutes=exam['margin'])), exams))
    return (filtered_exams)

@app.post('/exam')
async def exam(data: Exam):
    data.code = str(uuid4())
    db['Exam'].insert_one(jsonable_encoder(data))
    return ('exam_valid')

@app.post('/student')
async def student(data: Student):
    if db['Student'].find_one({'email': data.email}):
        return ('registration_error_email')
    db['Student'].insert_one(jsonable_encoder(data))
    return ('registration_valid')

@app.post('/attendance')
async def attendance(data: Attendance):
    student = db['Student'].find_one({'email': data.email})
    if not student:
        return ('attendance_error_email')
    if not validate_location(data.latitude, data.longitude, data.accuracy):
        return ('attendance_error_location')
    if not validate_face(student, data.image):
        return ('attendance_error_face')
    db['Attendance'].insert_one(jsonable_encoder(data))
    return ('attendance_valid')

def validate_location(latitude, longitude, accuracy):
    if accuracy > max_accuracy_allowed:
        return False
    distance = haversine((latitude, longitude), building_location, unit=Unit.METERS)
    if distance - accuracy > building_location_radius:
        return False
    return True

def validate_face(student, photo):
    result = DeepFace.verify(img1_path = student['image'], img2_path = photo)
    return result['verified'] 
