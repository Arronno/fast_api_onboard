from fastapi import FastAPI


fast_app = FastAPI()

@fast_app.get("/")
def landing_page():
    return {"message": "Landing Page!"}

@fast_app.get("/home")
def home():
    return {"message": "Welcome!"}
