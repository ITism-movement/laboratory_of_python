from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"Success": True}


@app.get("/ping2")
async def ping():
    return {"Success": True}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
