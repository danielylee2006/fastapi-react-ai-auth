from src.app import app

#Run uvicorn server only if we are running the server.py file directly instead of as module
if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)