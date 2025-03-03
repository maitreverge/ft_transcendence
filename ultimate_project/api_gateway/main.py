from fastapi import FastAPI, Request, WebSocket
import httpx
from fastapi.responses import HTMLResponse

app = FastAPI()

services = {
    "static_files": "http://static_files:8003",
    "tournament": "http://tournament:8001",
    "ws_tournament": "http://tournament:8001/ws/tournament",
    "ws_match": "http://match:8002/ws/match",
    "match": "http://match:8002",
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

@app.websocket("/ws/tournament/")
async def tournament_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print("message received: {data}")
            await websocket.send_text(f"Message text was: {data}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

@app.websocket("/ws/match/")
async def match_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print("message received: {data}")
            await websocket.send_text(f"Message text was: {data}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

# Probleme a regler:
# cliquer pour requete a "http://localhost:8000/tournament/simple-match/"
# ne passe pas par l'api_gateway!!!
@app.api_route("/tournament/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def tournament_proxy(path: str, request: Request):
    return await proxy_request("tournament", "tournament/" + path, request)

@app.api_route("/match/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def match_proxy(path: str, request: Request):
    return await proxy_request("match", "match/" + path, request)

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def static_files_proxy(path: str, request: Request):
    return await proxy_request("static_files", path, request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
