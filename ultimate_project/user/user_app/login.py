from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from os import getenv
from django.contrib.auth.models import User
from .forms import LoginForm
from urllib.parse import urlencode

def yes_login(request, context):
    return render(request, "user_app/yes_login.html", context)


def add(request):

    new_user = User()
    if request.method == "POST":
        # request.POST contains all the data the user submited
		# And we put it 
        form = LoginForm(request.POST)

        # Checking if the form is valid is making both a server side check even
        # if the client-side check seems to be valid.
		#! NEVER TRUST THE CLIENT
        # Imagine changing a form validation while client have the old html client-side checking
        if form.is_valid():
			# Extract the field named "task"
            username = request.POST["username"]
            password = request.POST["password"]

            print(f"Username ={username}\nPassword={password}")
			
            new_user.save()

            url = reverse("login:yes_login")
            query_string = urlencode({"username": username})
            return HttpResponseRedirect(f"{url}?{query_string}")
            
        else:
            return render(request, "user_app/login.html", {
				# If the form in invalid, we pass to the client the same form he tried to sumbit
				# So he can actually see what mistakes he made
                "form": form,
            })

    return render(request, "user_app/login.html", {
        "form" : LoginForm(),
    })


def sign_in(request):
    
    # cur_user = User()

    context = {
        # "uid" : getenv("AUTH_SECRET_42"),
        "form" : LoginForm()
    }

    return render(request, "user_app/signin.html", context)