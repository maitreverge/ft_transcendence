from django.shortcuts import render, redirect

# from django.http import HttpResponse
# from django.template import Context, Template
# from django.middleware import csrf
import requests
import os
import static_files.settings as settings
from django.http import JsonResponse

def index(request):
    username = request.session.get("username")
    if "HX-Request" not in request.headers:
        return redirect("/home/")
    obj = {"username": username, "request": request}
    return render(request, "index.html", obj)


def login_form(request):
    # csrf_token = csrf.get_token(request)
    return render(request, "landing_page.html")


def login(request):
    username = request.POST.get("username")
    request.session["username"] = username
    return redirect("/")


def home(request):
    if request.headers.get("HX-Request"):
        return render(request, "partials/home.html")
    username = request.session.get("username")
    obj = {"username": username, "page": "partials/home.html"}
    return render(request, "index.html", obj)


def profile(request):
    if request.headers.get("HX-Request"):
        return render(request, "partials/profile.html")
    username = request.session.get("username")
    obj = {"username": username, "page": "partials/profile.html"}
    return render(request, "index.html", obj)


def stats(request):
    if request.headers.get("HX-Request"):
        return render(request, "partials/stats.html")
    username = request.session.get("username")
    obj = {"username": username, "page": "partials/stats.html"}
    return render(request, "index.html", obj)


def match_simple_template(request, user_id):
    url = f"http://tournament:8001/tournament/simple-match/{user_id}/"
    print(f"###################### userid {user_id} #################", flush=True)
    page_html = requests.get(url).text
    username = request.session.get("username")
    return render(
        request,
        "index.html",
        {
            "username": username,
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),
            # "simpleUsers": consumer.players,
            "page": page_html,
        },
    )


def user_profile_template(request):
    page_html = requests.get("http://user:8004/user/profile/").text
    username = request.session.get("username")
    return render(
        request,
        "index.html",
        {
            "username": username,
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),
            # "simpleUsers": consumer.players,
            "page": page_html,
        },
    )


def user_stats_template(request):
    page_html = requests.get("http://user:8004/user/stats/").text
    username = request.session.get("username")
    return render(
        request,
        "index.html",
        {
            "username": username,
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),
            # "simpleUsers": consumer.players,
            "page": page_html,
        },
    )

def translations(request, lang):
    print("********** translations called **********", flush=True)
    try:
        file_path = os.path.join(settings.BASE_DIR, 'static_files_app', 'static', 'translations', f'{lang}.json')
        with open(file_path, 'r') as file:
            return JsonResponse(file.read(), safe=False)
    except FileNotFoundError:
        return JsonResponse({'error': 'File not found'}, status=404)
    