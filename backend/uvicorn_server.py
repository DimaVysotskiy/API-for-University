import uvicorn
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv(dotenv_path="../.env")  
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        workers=1,
    )