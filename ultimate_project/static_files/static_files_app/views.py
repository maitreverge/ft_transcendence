from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.middleware import csrf
from django.template import Context, Template


def index(request):
    username = request.session.get("username")
    return render(request, "index.html", {"username": username})


def login_form(request):
    csrf_token = csrf.get_token(request)
    return render(request, "login.html")
    template = Template(
        """
        <form hx-post="/login/" hx-target="body">
            {% csrf_token %}
            <input type="text" name="username" placeholder="Entrez votre nom">
            <button type="submit">Connexion</button>
        </form>
    """
    )
    context = Context({"csrf_token": csrf_token})
    return HttpResponse(template.render(context))


def login(request):
    username = request.POST.get("username")
    request.session["username"] = username
    return redirect("/")


def tournament(request):
    return HttpResponse(
        """
        <div class="overlay">
            <div class="overlay-content">
                <h2>Tournament creation</h2>
                <!-- Tournament content -->
                <button hx-get="/" hx-target="body">Close</button>
            </div>
        </div>
    """
    )


def simple_match(request):
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

def home(request):
    return render(request, "home.html")
