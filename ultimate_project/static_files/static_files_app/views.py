from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.middleware import csrf
from django.template import Context, Template
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.conf import settings

def set_language(request):
    print(f"set_language appelé avec méthode : {request.method}")  # DEBUG
    lang_code = request.POST.get("language")
    print(f"Langue demandée : {lang_code}")  # Vérifie si la langue est bien reçue
    if lang_code in dict(settings.LANGUAGES):  # Vérifie si la langue est valide
        request.session["django_language"] = lang_code  # Stocke en session
        activate(lang_code)  # Active immédiatement la langue dans la requête
        print(f"Langue changée : {lang_code}")  # Vérifie dans la console Django

    return redirect(request.META.get("HTTP_REFERER", "/"))  # Redirige vers la page précédente

def index(request):
    print(f"index appelé")  # Vérifie dans la console Django
    username = request.session.get("username")
    message = _("Hello, world!")
    return render(request, "index.html", {"username": username, "message": message})


def login_form(request):
    csrf_token = csrf.get_token(request)
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


# def tournament(request):
#     print(f"Tournament appelé", flush=True)  # Vérifie dans la console Django
#     return HttpResponse(
#         """
#         <div class="overlay">
#             <div class="overlay-content">
#                 <h2>Tournament creation</h2>
#                 <!-- Tournament content -->
#                 <button hx-get="/" hx-target="body">Close</button>
#             </div>
#         </div>
#     """
#     )


# def simple_match(request):
#     print(f"simple_match appelé")  # Vérifie dans la console Django
#     return HttpResponse(
#         """
#         <div class="overlay">
#             <div class="overlay-content">
#                 <h2>Simple Match</h2>
#                 <!-- match content -->
#                 <button hx-get="/" hx-target="body">Close</button>
#             </div>
#         </div>
#     """
#     )
