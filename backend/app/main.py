from fastapi_offline import FastAPIOffline

app = FastAPIOffline()


@app.get("/")
async def root():
    return {"message": "Hello World"}