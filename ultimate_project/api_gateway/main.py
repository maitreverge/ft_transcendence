from fastapi import FastAPI, Request
import httpx
from fastapi.responses import HTMLResponse

app = FastAPI()

services = {
    "static_files": "http://static_files:8003",
    "tournament": "http://tournament:8001",
    "match": "http://match:8002",
    "static_tournament": "http://tournament:8001/static/tournament",
}

async def proxy_request(service_name: str, path: str, request: Request):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        base_url = services[service_name].rstrip("/")
        path = path.lstrip("/")

        url = f"{base_url}/{path}"

        # print("\n**************** \n**************** PROXY API GATEWAY \n****************", url, "\n****************")
        headers = dict(request.headers)
        headers.pop("host", None)
        headers["Host"] = "localhost"

        method = request.method
        data = await request.body()

        response = await client.request(method, url, headers=headers, content=data)
        if response.headers.get("Content-Type", "").startswith("text/html"):
            return HTMLResponse(content=response.text)
        return response.text


# @app.api_route("/tournament/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
# @app.api_route("/tournament", methods=["GET", "POST", "PUT", "DELETE"])
# async def tournament_proxy(request: Request, path: str = ""):
#     full_path = f"/tournament/{path}" if path else "/tournament"
#     return await proxy_request("tournament", full_path, request)

@app.api_route("/tournament/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def tournament_proxy(path: str, request: Request):
    return await proxy_request("tournament", path, request)

@app.api_route("/static/tournament/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def tournament_proxy(path: str, request: Request):
    return await proxy_request("static_tournament", path, request)

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
