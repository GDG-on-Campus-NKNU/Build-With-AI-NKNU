import uvicorn

if __name__ == "__main__":
    # host="0.0.0.0" 使伺服器可從外部訪問，port 可自行調整
    uvicorn.run(app='main.server:app', host="0.0.0.0", port=8000, reload=True)
