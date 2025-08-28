from fastapi import FastAPI
from routes import planner, summarize, users, auth 

app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "AI Study Assistant Backend Running"}

app.include_router(summarize.router)
app.include_router(planner.router)  
