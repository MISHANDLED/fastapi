from fastapi import FastAPI
from . import models
from .database import engine
from .routes_to import users
from .routes_to import posts 
from .routes_to import auth 
from .routes_to import votes


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


# Entry Page
@app.get("/")
def message():
    
    return {"Message":"Hello World!",
            "Made By":"Devansh Mohata"}

