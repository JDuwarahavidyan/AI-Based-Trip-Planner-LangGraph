import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="AI Travel Planner",
    description="Agentic AI Travel Planner",
    version="0.1.0",
)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Travel Planner API"}    
