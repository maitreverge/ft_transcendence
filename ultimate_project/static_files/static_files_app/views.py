from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
import requests
import os
import static_files.settings as settings
from django.http import JsonResponse

def index(request):
    username = request.headers.get("X-Username")
    SERVER_IP = os.getenv('HOST_IP', '127.0.0.42')

    if "HX-Request" not in request.headers:
        return redirect("/home/")
    obj = {"username": username, "request": request}
    return render(request, "index.html", obj)

def login(request):
    obj = {"username": "", "page": "login.html"}
    return render(request, "index.html", obj)

def home(request):
    username = request.headers.get("X-Username") or request.session.get("username")

    if (
        request.headers.get("HX-Request")
        and request.headers.get("HX-Login-Success") != "true"
    ):
        return render(request, "partials/home.html", {"username": username, "host_ip": os.getenv('HOST_IP')})

    obj = {"username": username, "page": "partials/home.html", "host_ip": os.getenv('HOST_IP')}
    return render(request, "index.html", obj)

def reload_template(request):
    
    """
    The purpose of `reload_template` is to enable full page reloading while serving 
    dynamic content through the static container. 

    This function is specifically triggered when a service is requested to be served 
    through the static container, as defined in the `reverse_proxy_request` function 
    of the FastAPI app. 
    
    """
    headers = {}
    for key, value in request.headers.items():
        if key != "HX-Request":
            headers[key] = value
    url = headers["X-Url-To-Reload"]
    username = request.headers.get("X-Username")
    context = {"username": username}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        page_html = response.text
    else:
        code = response.status_code
        username = request.session.get("username")
        context["status_code"] = code
        context["page"] = "error.html"
        return render(request, "index.html", context)
    username = request.headers.get("X-Username") or request.session.get("username")
    context["page"] = page_html
    return render(request, "index.html", context)


def match_simple_template(request, user_id):
    url = f"http://tournament:8001/tournament/simple-match/{user_id}/"
    page_html = requests.get(url).text

    username = request.headers.get("X-Username") or request.session.get("username")

    return render(
        request,
        "index.html",
        {
            "username": username,
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("HOST_IP", "localhost:8443"),
            "page": page_html,
        },
    )


def tournament_template(request, user_id):
    url = f"http://tournament:8001/tournament/tournament/{user_id}/"
    page_html = requests.get(url).text

    username = request.headers.get("X-Username") or request.session.get("username")

    return render(
        request,
        "index.html",
        {
            "username": username,
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("HOST_IP", "localhost:8443"),
            "page": page_html,
        },
    )


def translations(request, lang):
    try:
        file_path = os.path.join(
            settings.BASE_DIR,
            "static_files_app",
            "static",
            "translations",
            f"{lang}.json",
        )
        with open(file_path, "r") as file:
            return JsonResponse(file.read(), safe=False)
    except FileNotFoundError:
        return JsonResponse({"error": "File not found"}, status=404)


def register(request):
    username = request.headers.get("X-Username") or request.session.get("username")

    obj = {"username": username, "page": "register.html"}
    return render(request, "index.html", obj)


def twoFactorAuth(request):
    username = request.headers.get("X-Username") or request.session.get("username")

    query_username = request.GET.get("username")
    if query_username:
        username = query_username

    if "HX-Request" in request.headers:
        return render(request, "two-factor-auth.html", {"username": username})

    obj = {"username": username, "page": "two-factor-auth.html"}
    return render(request, "index.html", obj)

@csrf_exempt    
def error(request, code=404):
    username = request.session.get("username")
    obj = {"username": username, "status_code": code, "page": "error.html"}
    return render(request, "index.html", obj)
