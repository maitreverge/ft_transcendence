from fastapi import FastAPI, Request, WebSocket
import httpx
from fastapi.responses import HTMLResponse

app = FastAPI()

services = {
    "static_files": "http://static_files:8003",
    "tournament": "http://tournament:8001",
    "match": "http://match:8002",
    "ws_tournament": "http://tournament:8001/ws/tournament",
}

async def proxy_request(service_name: str, path: str, request: Request):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        base_url = services[service_name].rstrip("/")
        path = path.lstrip("/")
        url = f"{base_url}/{path}"

        headers = dict(request.headers)
        headers.pop("host", None)
        headers["Host"] = "localhost"

        method = request.method
        data = await request.body()

        response = await client.request(method, url, headers=headers, content=data)
        if response.headers.get("Content-Type", "").startswith("text/html"):
            return HTMLResponse(content=response.text)
        return response.text


# 	location /ws/tournament/ {
# 		proxy_pass http://ctn_tournament:8001/ws/tournament/; 
# 		proxy_http_version 1.1;                 # ✅ WebSocket nécessite HTTP 1.1
#         proxy_set_header Upgrade $http_upgrade; # ✅ Indique que c'est un WebSocket
#         proxy_set_header Connection "Upgrade";  # ✅ Autorise la montée en protocole
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
# 	}

@app.websocket("/ws/tournament/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

@app.api_route("/ws/tournament/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def tournament_proxy(path: str, request: Request):
    return await proxy_request("ws_tournament", path, request)

@app.api_route("/tournament/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def tournament_proxy(path: str, request: Request):
    return await proxy_request("tournament", path, request)

@app.api_route("/match/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def match_proxy(path: str, request: Request):
    return await proxy_request("match", path, request)

    # @app.api_route("/user/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    # async def user_proxy(path: str, request: Request):
    #     return await proxy_request("user", path, request)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def static_files_proxy(path: str, request: Request):
    return await proxy_request("static_files", path, request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
