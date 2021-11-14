from fastapi import FastAPI
from . import models
from .database import engine
from .routes_to import users as u
from .routes_to import posts as p
from .routes_to import auth 


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(p.router)
app.include_router(u.router)
app.include_router(auth.router)


# Entry Page
@app.get("/")
def message():
    
    return {"Message":"Hello World!",
            "Made By":"Devansh Mohata"}

