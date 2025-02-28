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


from fastapi import FastAPI, Request, HTTPException
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
async def proxy_request(service_name: str, path: str, request: Request):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        base_url = services[service_name].rstrip("/")  # S'assurer que pas de double "/"
        path = path.lstrip("/")  # Supprime "/" initial pour éviter "//" dans l’URL

        # print(f"\n&&&&& before: Proxying request to: {base_url} &&&&&\n")  # <---- AJOUTE CE LOG
        url = f"{base_url}/{path}"  # Construit proprement l’URL
        # print(f"\n&&&&& after: Proxying request to: {url} &&&&&\n")  # <---- AJOUTE CE LOG

        headers = dict(request.headers)
        headers.pop("host", None)  # Retire "Host" en-tête
        headers["Host"] = "localhost"

        method = request.method
        data = await request.body()

        # print(f"\n*************🔎 Proxy request to: {url} *******************\n")  # Debugging

        response = await client.request(method, url, headers=headers, content=data)
        if response.headers.get("Content-Type", "").startswith("text/html"):
            return HTMLResponse(content=response.text)
        return response.text


@app.api_route("/tournament/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/tournament", methods=["GET", "POST", "PUT", "DELETE"])
async def tournament_proxy(request: Request, path: str = ""):
    full_path = f"/tournament/{path}" if path else "/tournament"
    return await proxy_request("tournament", full_path, request)

@app.api_route("/tournament/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def tournament_proxy(path: str, request: Request):
    return await proxy_request("tournament", path, request)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def static_files_proxy(path: str, request: Request):
    print(f"🔥 Received static file request: {path}")  # <--- LOG
    return await proxy_request("static_files", path, request)

@app.api_route("/match/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def match_proxy(path: str, request: Request):
    return await proxy_request("match", path, request)

@app.api_route("/user/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def user_proxy(path: str, request: Request):
    return await proxy_request("user", path, request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
