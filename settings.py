import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONGODB_KEY = config('MONGODB_KEY')
BACKEND_URL = config('BACKEND_URL')
