from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone

from deepface import DeepFace
from haversine import haversine, Unit
from uuid import uuid4

from settings import MONGODB_KEY, FRONTEND_URL

from enum import Enum

class Result(str, Enum):
    STUDENT_ERROR_AUTH = 'student_error_auth'
    EXAM_ERROR_AUTH = 'exam_error_auth'
    ATTENDANCE_ERROR_AUTH = 'attendance_error_auth'
    EXAM_VALID = 'exam_valid'
    REGISTRATION_ERROR_EMAIL = 'registration_error_email'
    REGISTRATION_VALID = 'registration_valid'
    ATTENDANCE_ERROR_EMAIL = 'attendance_error_email'
    ATTENDANCE_ERROR_LOCATION = 'attendance_error_location'
    ATTENDANCE_ERROR_FACE = 'attendance_error_face'
    ATTENDANCE_VALID = 'attendance_valid'
    EXAM_ERROR_CODE = 'exam_error_code'
    EXAM_UPDATE = 'exam_update'

    def __str__(self):
        return self.value

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
async def exam(filter: bool):
    filter_expression = build_filter_expression() if filter else {}
    exams = list(db['Exam'].find(filter_expression, {'_id': False})) 
    return (exams)

@app.get('/attendance')
async def attendance(code: str):
    attendances = list(db['Attendance'].find({'code': code}, {'_id': False, 'image': False}))
    return (attendances)

@app.post('/exam')
async def exam(data: Exam, request: Request):
    token = request.headers.get('Authorization')
    if token == '' and False:
        return (Result.EXAM_ERROR_AUTH)
    data.code = str(uuid4())
    db['Exam'].insert_one(jsonable_encoder(data))
    return (Result.EXAM_VALID)

@app.post('/student')
async def student(data: Student, request: Request):
    token = request.headers.get('Authorization')
    if token == '' and False:
        return (Result.STUDENT_ERROR_AUTH)
    if db['Student'].find_one({'email': data.email}):
        return (Result.REGISTRATION_ERROR_EMAIL)
    db['Student'].insert_one(jsonable_encoder(data))
    return (Result.REGISTRATION_VALID)

@app.post('/attendance')
async def attendance(data: Attendance, request: Request):
    token = request.headers.get('Authorization')
    if token == '' and False:
        return (Result.ATTENDANCE_ERROR_AUTH)
    student = db['Student'].find_one({'email': data.email})
    if not student:
        return (Result.ATTENDANCE_ERROR_EMAIL)
    if not validate_location(data.latitude, data.longitude, data.accuracy):
        return (Result.ATTENDANCE_ERROR_LOCATION)
    if not validate_face(student, data.image):
        return (Result.ATTENDANCE_ERROR_FACE)
    db['Attendance'].insert_one(jsonable_encoder(data))
    return (Result.ATTENDANCE_VALID)

@app.put('/exam') 
async def exam(data: Exam, request: Request):
    token = request.headers.get('Authorization')
    if token == '' and False:
        return (Result.EXAM_ERROR_AUTH)
    result = db['Exam'].update_one({"code": data.code}, {"$set": jsonable_encoder(data)})
    if result.modified_count == 0:
        return (Result.EXAM_ERROR_CODE)
    return (Result.EXAM_UPDATE)
    
def validate_location(latitude, longitude, accuracy):
    # Temporalmente se remueve la verificación de ubicación para facilitar el desarrollo
    return True
    if accuracy > max_accuracy_allowed:
        return False
    distance = haversine((latitude, longitude), building_location, unit=Unit.METERS)
    if distance - accuracy > building_location_radius:
        return False
    return True

def validate_face(student, photo):
    # Temporalmente se remueve la verificación de rostro por problemas de infraestructura
    #result = DeepFace.verify(img1_path = student['image'], img2_path = photo)
    result = {'verified': True}
    return result['verified'] 

def build_filter_expression():
    return {
        '$expr': {
            '$and': [
                {
                    '$gte': [
                        datetime.now(),
                        {
                            "$dateAdd": {
                                "startDate": {"$toDate": "$start"},
                                "unit": "minute",
                                "amount": {"$multiply": ["$margin", -1]}
                            }
                        }
                    ]
                },
                {
                    '$lte': [
                        datetime.now(),
                        {
                            "$dateAdd": {
                                "startDate": {"$toDate": "$start"},
                                "unit": "minute",
                                "amount": "$margin"
                            }
                        }
                    ]
                }
            ]
        }
    }
