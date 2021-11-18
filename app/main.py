from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routes_to import users
from .routes_to import posts 
from .routes_to import auth 
from .routes_to import votes


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


# Entry Page
@app.get("/")
def message():
    
    return {"Message":"Hello World!",
            "Made By":"Devansh Mohata"}

