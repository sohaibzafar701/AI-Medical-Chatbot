from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
import sqlite3
import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your_secure_key_here")  # Default for testing
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="../frontend/")

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database setup
def get_db_connection():
    conn = sqlite3.connect("chatbot.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

create_tables()

# Pydantic Models
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility Functions
def get_user(username: str):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

def create_user(username: str, password: str):
    hashed_password = password_context.hash(password)
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(f"Received token: {token}")  # Debug
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")  # Debug
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Error: {e}")  # Debug
        raise credentials_exception

    user = get_user(username)
    if user is None:
        print(f"User not found: {username}")  # Debug
        raise credentials_exception
    return {"id": user["id"], "username": user["username"]}


def log_query(user_id: int, query: str, response: str):
    conn = get_db_connection()
    conn.execute("INSERT INTO logs (user_id, query, response) VALUES (?, ?, ?)", (user_id, query, response))
    conn.commit()
    conn.close()

# ChromaDB Setup
client = chromadb.PersistentClient(path="C:/Users/sohaib/Downloads/medical-chatbot-main/medical-chatbot-main/dataset/chromadb")
collection = client.get_collection(name="medquad")

# API Endpoints
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register")
def get_register(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chatbot")
def chatbot_query(query: str, user: dict = Depends(get_current_user)):
    results = collection.query(query_texts=[query], n_results=3)
    if results["documents"] and results["metadatas"]:
        response = results["metadatas"][0][0].get("answer", f"AI Response to: {query}")
    else:
        response = f"No specific information found for: {query}. Please consult a healthcare professional."
    log_query(user["id"], query, response)
    return {"query": query, "response": response, "user": user["username"]}


@app.post("/register")
def register(user: UserCreate):
    create_user(user.username, user.password)
    return {"message": "User registered successfully"}

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
