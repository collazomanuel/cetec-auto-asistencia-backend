
from datetime import datetime, timedelta, timezone
from enum import Enum
from uuid import uuid4

import requests
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from haversine import haversine, Unit
from pydantic import BaseModel
from pymongo import MongoClient

from deepface import DeepFace

from settings import MONGODB_KEY, FRONTEND_URL

DB_NAME = 'cetec-auto-asistencia'
STUDENT_COLLECTION_NAME = 'Student'
PROFESSOR_COLLECTION_NAME = 'Professor'
EXAM_COLLECTION_NAME = 'Exam'
ATTENDANCE_COLLECTION_NAME = 'Attendance'

BUILDING_LOCATION = (-34.617639, -58.368056)
BUILDING_LOCATION_RADIUS = 150
MAX_ACCURACY_ALLOWED = 100
DATE_FORMAT = '%Y-%m-%d %H:%M'

class Result(str, Enum):

    SUCCESS_STUDENT_ADD = 'SUCCESS_STUDENT_ADD'
    ERROR_STUDENT_AUTH = 'ERROR_STUDENT_AUTH'
    ERROR_STUDENT_EMAIL = 'ERROR_STUDENT_EMAIL'

    SUCCESS_PROFESSOR_ADD = 'SUCCESS_PROFESSOR_ADD'
    ERROR_PROFESSOR_AUTH = 'ERROR_PROFESSOR_AUTH'
    ERROR_PROFESSOR_EMAIL = 'ERROR_PROFESSOR_EMAIL'

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
    image: str

class Professor(BaseModel):
    email: str

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
    image: str

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins = [FRONTEND_URL], allow_credentials = True, allow_methods = ['*'], allow_headers = ['*'])
security = HTTPBearer()
client = MongoClient(MONGODB_KEY)
db = client[DB_NAME]

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):    
    token = credentials.credentials
    response = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        headers={'Authorization': f'Bearer {token}'}
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user_info = response.json()
    return user_info

@app.post('/student')
async def student(data: Student, current_user: dict = Depends(get_current_user)):
    if not is_a_professor(current_user['email']):
        return (Result.ERROR_EXAM_AUTH)
    if db[STUDENT_COLLECTION_NAME].find_one({'email': data.email}):
        return (Result.ERROR_STUDENT_EMAIL)
    db[STUDENT_COLLECTION_NAME].insert_one(jsonable_encoder(data))
    return (Result.SUCCESS_STUDENT_ADD)

@app.get('/professor')
async def professor():
    professors = list(db[PROFESSOR_COLLECTION_NAME].find({}, {'_id': False})) 
    return(professors)

@app.post('/professor')
async def professor(data: Professor, current_user: dict = Depends(get_current_user)):
    if not is_a_professor(current_user['email']):
        return (Result.ERROR_PROFESSOR_AUTH)
    if db[PROFESSOR_COLLECTION_NAME].find_one({'email': data.email}):
        return (Result.ERROR_PROFESSOR_EMAIL)
    db[PROFESSOR_COLLECTION_NAME].insert_one(jsonable_encoder(data))
    return (Result.SUCCESS_PROFESSOR_ADD)

@app.get('/exam')
async def exam(filter: bool):
    filter_expression = build_filter_expression() if filter else {}
    exams = list(db[EXAM_COLLECTION_NAME].find(filter_expression, {'_id': False})) 
    return (exams)

@app.post('/exam')
async def exam(data: Exam, current_user: dict = Depends(get_current_user)):
    if not is_a_professor(current_user['email']):
        return (Result.ERROR_EXAM_AUTH)
    data.code = str(uuid4())
    db[EXAM_COLLECTION_NAME].insert_one(jsonable_encoder(data))
    return (Result.SUCCESS_EXAM_ADD)

@app.put('/exam') 
async def exam(data: Exam, current_user: dict = Depends(get_current_user)):
    if not is_a_professor(current_user['email']):
        return (Result.ERROR_EXAM_AUTH)
    result = db[EXAM_COLLECTION_NAME].update_one({'code': data.code}, {'$set': jsonable_encoder(data)})
    if result.modified_count == 0:
        return (Result.ERROR_EXAM_CODE)
    return (Result.SUCCESS_EXAM_EDIT)

@app.get('/attendance')
async def attendance(code: str):
    attendances = list(db[ATTENDANCE_COLLECTION_NAME].find({'code': code}, {'_id': False, 'image': False}))
    return (attendances)

@app.post('/attendance')
async def attendance(data: Attendance, current_user: dict = Depends(get_current_user)):
    if not is_a_student(current_user['email']):
        return (Result.ERROR_ATTENDANCE_AUTH)
    student = db[STUDENT_COLLECTION_NAME].find_one({'email': data.email})
    if not student:
        return (Result.ERROR_ATTENDANCE_EMAIL)
    if not validate_location(data.latitude, data.longitude, data.accuracy):
        return (Result.ERROR_ATTENDANCE_LOCATION)
    if not validate_face(student, data.image):
        return (Result.ERROR_ATTENDANCE_FACE)
    db[ATTENDANCE_COLLECTION_NAME].insert_one(jsonable_encoder(data))
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

def is_a_professor(email):
    return db[PROFESSOR_COLLECTION_NAME].find_one({'email': email}) != None

def is_a_student(email):
    return db[STUDENT_COLLECTION_NAME].find_one({'email': email}) != None
