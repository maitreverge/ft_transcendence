from fastapi import FastAPI

app = FastAPI()

@app.get("/api_gateway/")
def read_root():
    return {"message": "API Gateway is running"}

@app.get("/tournament/")
def tournament():
    return {"message": "Tournament route"}

@app.get("/test/")
def test():
    return {"message": "Test route"}

@app.get("/match/")
def match():
    return {"message": "Match route"}

@app.get("/user/")
def user():
    return {"message": "User route"}

@app.get("/static/static_files/")
def static_files():
    return {"message": "Static files"}

@app.get("/ws/")
async def websocket_endpoint():
    return {"message": "WebSocket route"}

# Ajoute d'autres routes si nécessaire

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)


