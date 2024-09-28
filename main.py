import uvicorn

from fastapi import FastAPI
from app.routers import users, tasks

app = FastAPI(title="GoKapture")

# Including users and tasks routers
app.include_router(users.router)
app.include_router(tasks.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
