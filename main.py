import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller.file_endpoints import router as endpoints_v1
from controller.file_endpoints_v2 import router as endpoints_v2

app = FastAPI()

app.include_router(endpoints_v1)
app.include_router(endpoints_v2)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
