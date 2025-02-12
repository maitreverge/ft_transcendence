from django.shortcuts import render
from django.http import HttpResponse


def test(request):
    return render(request, "user.html", {"test": "COUCOU CONNEXION"})


# Create your views here.
def login(request):

    url_42 = f"https://api.intra.42.fr/oauth/authorize?client_id={getenv(AUTH_UDI_42)}&redirect"

    return HttpResponse(
        """
       <h1> HELLO CONNEXION PAGE </h1>
       <h1> HELLO CONNEXION PAGE </h1>
       <h1> HELLO CONNEXION PAGE </h1>
       <h1> HELLO CONNEXION PAGE </h1>
       <h1> HELLO CONNEXION PAGE </h1>
       <h1> HELLO CONNEXION PAGE </h1>
    """
    )
