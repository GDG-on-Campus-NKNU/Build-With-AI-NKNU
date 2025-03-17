from fastapi import FastAPI, Response
import uvicorn

app = FastAPI()

@app.get("/test") # Route: /test
async def test(response: Response):
    response.status_code = 200
    return {"message": "Hello, FastAPI! Test is here."}

@app.get("/") # Route: /
async def root(response: Response):
    response.status_code = 200
    return {"message": "Welcome to FastAPI!"}

if __name__ == "__main__":
    # host="0.0.0.0" 使伺服器可從外部訪問，port 可自行調整
    uvicorn.run(app='app', host="0.0.0.0", port=8000, reload=True)