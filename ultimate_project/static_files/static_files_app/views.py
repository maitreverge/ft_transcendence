from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.middleware import csrf
from django.template import Context, Template
import json
from django.http import JsonResponse
import os
from django.conf import settings


def index(request):
    print("********** index called **********", flush=True)
    username = request.session.get("username")
    return render(request, "index.html", {"username": username})


def login_form(request):
    print("********** login_form called **********", flush=True)
    csrf_token = csrf.get_token(request)
    template = Template(
        """
        <form hx-post="/login/" hx-target="body">
            {% csrf_token %}
            <input type="text" name="username" placeholder=""  data-translate="login_placeholder">
            <button type="submit" data-translate="login_button"></button>
        </form>
    """
    )
    context = Context({"csrf_token": csrf_token})
    return HttpResponse(template.render(context))


def login(request):
    print("********** login called **********", flush=True)
    username = request.POST.get("username")
    request.session["username"] = username
    return redirect("/")

def simple_match(request):
    print("********** simple_match called **********", flush=True)
    return HttpResponse(
        """
        <div class="overlay">
            <div class="overlay-content">
                <h2>Simple Match</h2>
                <!-- match content -->
                <button hx-get="/" hx-target="body">Close</button>
            </div>
        </div>
    """
    )

def translations(request, lang):
    print("********** translations called **********", flush=True)
    try:
        file_path = os.path.join(settings.BASE_DIR, 'static', 'translations', f'{lang}.json')
        with open(file_path, 'r') as file:
            return JsonResponse(file.read(), safe=False)
    except FileNotFoundError:
        return JsonResponse({'error': 'File not found'}, status=404)
