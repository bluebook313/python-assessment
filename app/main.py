from fastapi import FastAPI
from api import router as api_router

import uvicorn

app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",          # module:app_instance
        host="0.0.0.0",
        port=8000,
        reload=True,         # auto-reload on code changes
    )