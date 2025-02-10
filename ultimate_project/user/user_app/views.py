from django.shortcuts import render
from django.http import HttpResponse


def test(request):
    return render(request, "user.html", {"test": "COUCOU CONNEXION"})


# Create your views here.
def login(request):
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
