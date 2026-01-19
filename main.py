from Database import get_connection
from pydantic import BaseModel
from passlib.context import CryptContext

# lines 3 - 15 were taken from a YouTube video on Fast API and Flutter CRUD Application
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "EcoPocket"}

class VoucherIn(BaseModel):
    voucher_code: str

class RegisterIn(BaseModel):
    name: str
    email: str
    password: str

class LoginIn(BaseModel):
    email: str
    password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# some of the following code was taken adjusted from a 'tecadmin' webpage
# and some was taken and adjusted from a ChatGPT conversation
@app.get("/voucher")
def get_vouchers():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT * FROM voucher"""
    cursor.execute(query)
    voucher = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"voucher": voucher}

@app.post("/voucher")
def add_voucher(voucher: VoucherIn):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "INSERT INTO voucher (voucher_code) VALUES (%s)"
    cursor.execute(query, (voucher.voucher_code,))
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": f"Voucher {voucher.voucher_code} added successfully."}

@app.post("/register")
def register(user: RegisterIn):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    query = """
        INSERT INTO users (name, email, password, total_refunds)
        VALUES (%s, %s, %s, 0.00)
    """
    cursor.execute(query, (user.name, user.email, hashed_password))
    connection.commit()

    cursor.close()
    connection.close()

    return {"success": True, "message": "User registered successfully"}

@app.post("/login")
def login(user: LoginIn):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "success": True,
        "user_id": db_user["user_id"],
        "name": db_user["name"],
        "total_refunds": float(db_user["total_refunds"])
    }

