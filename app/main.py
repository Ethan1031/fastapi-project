from fastapi import FastAPI, status
from . import models
from .database import engine
from .routers import user, post, auth, vote

from fastapi.middleware.cors import CORSMiddleware

# Use this command to create all table when we first run it, but now we using alembic, so no longer need it
# models.Base.metadata.create_all(bind = engine)

app = FastAPI()

# Set the specific domains that allows to talk to us. 
# origins = ["https://www.google.com"]

# Set domains to all.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Clean our main.py file, put all code in separate file, then call router as path to access them
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Hello World"}

