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

    SUCCESS_STUDENT_ADD = 'SUCCESS_STUDENT_ADD'
    ERROR_STUDENT_AUTH = 'ERROR_STUDENT_AUTH'
    ERROR_STUDENT_EMAIL = 'ERROR_STUDENT_EMAIL'

    SUCCESS_EXAM_ADD = 'SUCCESS_EXAM_ADD'
    SUCCESS_EXAM_EDIT = 'SUCCESS_EXAM_EDIT'
    ERROR_EXAM_AUTH = 'ERROR_EXAM_AUTH'
    ERROR_EXAM_CODE = 'ERROR_EXAM_CODE'

    SUCCESS_ATTENDANCE_ADD = 'SUCCESS_ATTENDANCE_ADD'
    ERROR_ATTENDANCE_AUTH = 'ERROR_ATTENDANCE_AUTH'
    ERROR_ATTENDANCE_EMAIL = 'ERROR_ATTENDANCE_EMAIL'
    ERROR_ATTENDANCE_LOCATION = 'ERROR_ATTENDANCE_LOCATION'
    ERROR_ATTENDANCE_FACE = 'ERROR_ATTENDANCE_FACE'

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

BUILDING_LOCATION = (-34.617639, -58.368056)
BUILDING_LOCATION_RADIUS = 150
MAX_ACCURACY_ALLOWED = 100
DATE_FORMAT = '%Y-%m-%d %H:%M'

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins = [FRONTEND_URL], allow_credentials = True, allow_methods = ['*'], allow_headers = ['*'])
client = MongoClient(MONGODB_KEY)
db = client['cetec-auto-asistencia']

@app.post('/student')
async def student(data: Student, request: Request):
    token = request.headers.get('Authorization')
    if token == '' and False:
        return (Result.ERROR_STUDENT_AUTH)
    if db['Student'].find_one({'email': data.email}):
        return (Result.ERROR_STUDENT_EMAIL)
    db['Student'].insert_one(jsonable_encoder(data))
    return (Result.SUCCESS_STUDENT_ADD)

@app.get('/exam')
async def exam(filter: bool):
    filter_expression = build_filter_expression() if filter else {}
    exams = list(db['Exam'].find(filter_expression, {'_id': False})) 
    return (exams)

@app.post('/exam')
async def exam(data: Exam, request: Request):
    token = request.headers.get('Authorization')
    if token == '' and False:
        return (Result.ERROR_EXAM_AUTH)
    data.code = str(uuid4())
    db['Exam'].insert_one(jsonable_encoder(data))
    return (Result.SUCCESS_EXAM_ADD)

@app.put('/exam') 
async def exam(data: Exam, request: Request):
    token = request.headers.get('Authorization')
    if token == '' and False:
        return (Result.ERROR_EXAM_AUTH)
    result = db['Exam'].update_one({'code': data.code}, {'$set': jsonable_encoder(data)})
    if result.modified_count == 0:
        return (Result.ERROR_EXAM_CODE)
    return (Result.SUCCESS_EXAM_EDIT)

@app.get('/attendance')
async def attendance(code: str):
    attendances = list(db['Attendance'].find({'code': code}, {'_id': False, 'image': False}))
    return (attendances)

@app.post('/attendance')
async def attendance(data: Attendance, request: Request):
    token = request.headers.get('Authorization')
    if token == '' and False:
        return (Result.ERROR_ATTENDANCE_AUTH)
    student = db['Student'].find_one({'email': data.email})
    if not student:
        return (Result.ERROR_ATTENDANCE_EMAIL)
    if not validate_location(data.latitude, data.longitude, data.accuracy):
        return (Result.ERROR_ATTENDANCE_LOCATION)
    if not validate_face(student, data.image):
        return (Result.ERROR_ATTENDANCE_FACE)
    db['Attendance'].insert_one(jsonable_encoder(data))
    return (Result.SUCCESS_ATTENDANCE_ADD)
    
def validate_location(latitude, longitude, accuracy):
    # Temporalmente se remueve la verificación de ubicación para facilitar el desarrollo
    return True
    if accuracy > MAX_ACCURACY_ALLOWED:
        return False
    distance = haversine((latitude, longitude), BUILDING_LOCATION, unit=Unit.METERS)
    if distance - accuracy > BUILDING_LOCATION_RADIUS:
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
                            '$dateAdd': {
                                'startDate': {'$toDate': '$start'},
                                'unit': 'minute',
                                'amount': {'$multiply': ['$margin', -1]}
                            }
                        }
                    ]
                },
                {
                    '$lte': [
                        datetime.now(),
                        {
                            '$dateAdd': {
                                'startDate': {'$toDate': '$start'},
                                'unit': 'minute',
                                'amount': '$margin'
                            }
                        }
                    ]
                }
            ]
        }
    }
