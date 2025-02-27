# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/api_gateway/")
# def read_root():
#     return {"message": "API Gateway is running"}

# @app.get("/tournament/")
# def tournament():
#     return {"message": "Tournament route"}

# @app.get("/test/")
# def test():
#     return {"message": "Test route"}

# @app.get("/match/")
# def match():
#     return {"message": "Match route"}

# @app.get("/user/")
# def user():
#     return {"message": "User route"}

# @app.get("/static/static_files/")
# def static_files():
#     return {"message": "Static files"}

# @app.get("/ws/")
# async def websocket_endpoint():
#     return {"message": "WebSocket route"}

# # Ajoute d'autres routes si nécessaire

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8005)


from fastapi import FastAPI
import httpx
from fastapi.responses import HTMLResponse

app = FastAPI()

# Définition des containers
services = {
    "static_files": "http://static_files:8003",
    "tournament": "http://tournament:8001",
    "match": "http://match:8002",
}

# Fonction pour proxy une requête
async def proxy_request(service_name: str, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{services[service_name]}{path}"
        response = await client.get(url)
        if response.headers.get("Content-Type", "").startswith("text/html"):
            return HTMLResponse(content=response.text)
        return response.text

@app.get("/tournament/{path:path}")
async def tournament_proxy(path: str):
    return await proxy_request("tournament", f"/tournament/{path}")

@app.get("/{path:path}")
async def tournament_proxy(path: str):
    return await proxy_request("static_files", f"/{path}")

@app.get("/match/{path:path}")
async def match_proxy(path: str):
    return await proxy_request("match", f"/match/{path}")

@app.get("/user/{path:path}")
async def user_proxy(path: str):
    return await proxy_request("user", f"/user/{path}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
