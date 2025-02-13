from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import LoginForm

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def yes_login(request):
    return render(request, "user_app/yes_login.html")


def add(request):

    for _ in range(10):
        print("HERE")
    logger.info(request.POST) 

    new_user = User()
    if request.method == "POST":
        # request.POST contains all the data the user submited
		# And we put it 
        form = LoginForm(request.POST)

        logger.info(request.POST) 

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

            # url = reverse("login:yes_login")
            # query_string = urlencode({"username": username})
            return HttpResponseRedirect(reverse("login:yes_login"))
            
        else:
            return render(request, "user_app/signin.html", {
				# If the form in invalid, we pass to the client the same form he tried to sumbit
				# So he can actually see what mistakes he made
                "form": form,
                "message" : "form not valid",
            })

    return render(request, "user_app/signin.html", {
        "form" : LoginForm(),
        "message" : "not post request",
    })


def sign_in(request):
    
    # cur_user = User()

    context = {
        # "uid" : getenv("AUTH_SECRET_42"),
        "form" : LoginForm()
    }

    return render(request, "user_app/signin.html", context)