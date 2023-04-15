# coding: utf-8
#Rebar Application Settings Service settings.py 

from pathlib import Path
from decouple import config
from httpx import (Timeout, Limits)
from starlette.templating import Jinja2Templates

# Platform Directory Paths
BASE_DIR = Path(__file__).parent
HOME_DIR = Path(__file__).parent.parent
STATIC_PATH = Path.joinpath(HOME_DIR, 'static')
DOCUMENT_PATH = Path.joinpath(STATIC_PATH, 'docs')
UPLOADS_PATH = Path.joinpath(STATIC_PATH, 'uploads')

IMAGES_PATH = Path.joinpath(STATIC_PATH, 'imgs')
WORKER_PROFILE_PATH = Path.joinpath(STATIC_PATH, 'imgs', 'workers')
PRODUCTS_PROFILE_PATH = Path.joinpath(STATIC_PATH, 'imgs', 'products')
PLATFORM_PROFILE_PATH = Path.joinpath(STATIC_PATH, 'imgs', 'platform')
BACKGROUNDS_PROFILE_PATH = Path.joinpath(STATIC_PATH, 'imgs', 'bgs')

TEMPLATES_PATH = Path.joinpath(HOME_DIR, 'templates')
CERT_DIR = Path.joinpath(HOME_DIR, '.ssl')
LOGS_DIR = Path.joinpath(HOME_DIR, 'logs')

# Authentication and Access
SERVER_CERT = Path.joinpath(CERT_DIR, 'revue.crt')
SERVER_PEM = Path.joinpath(CERT_DIR, 'revue.pem')
SECRET_KEY = None #config('SECRET_KEY')
DB_ADMIN = config('dbAdmin')
ADMIN_ACCESS = config('adminAccess')



DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = ''
USE_L10N = True

HEADERS = {'user-agent': 'rebar/0.0.1', 'Content-Type': 'application/json'}
TIMEOUT = Timeout(10.0, connect=60.0)
LIMITS = Limits(max_keepalive_connections=5, max_connections=10)
MAX_REDIRECTS:int = 1
# Network
HOST = '0.0.0.0'
PORT = 8080

# Templates
templates = Jinja2Templates(directory=TEMPLATES_PATH)

def skg():    
    from modules.utils import GenerateId
    try: return GenerateId().gen_id('app')
    except Exception:  print(str(Exception))
    finally: del GenerateId

# Server keys
SECRET_KEY = skg()
KEY_STORE = {'',}

# logs
SERVER_LOG = Path.joinpath(LOGS_DIR, 'server.log')
SYSTEM_LOG = Path.joinpath(LOGS_DIR, 'system.log')
APP_LOG = Path.joinpath(LOGS_DIR, 'app.log')

# Files
ALLOWED_FILE_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'}

