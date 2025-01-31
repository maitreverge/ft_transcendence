from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    username = "username"
    return render(request, 'index.html', {'username': username})

def login_form(request):
    return HttpResponse("""
        <form hx-post="/login/" hx-target="body">
            <input type="text" name="username" placeholder="Entrez votre nom">
            <button type="submit">Connexion</button>
        </form>
    """)

def login(request):
    username = request.POST.get('username')
    username = "username"
    return redirect('/')

def tournament(request):
    return HttpResponse("""
        <div class="overlay">
            <div class="overlay-content">
                <h2>Tournament creation</h2>
                <!-- Tournament content -->
                <button hx-get="/" hx-target="body">Close</button>
            </div>
        </div>
    """)

def simple_match(request):
    return HttpResponse("""
        <div class="overlay">
            <div class="overlay-content">
                <h2>Simple Match</h2>
                <!-- match content -->
                <button hx-get="/" hx-target="body">Close</button>
            </div>
        </div>
    """)
