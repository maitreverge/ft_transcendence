from django.shortcuts import render
from django.http import HttpResponse
from os import getenv


def oauth_42(request):
    # =>
    # ? STEP 1 : get access to the 42 auth page

    context = {
        "uid" : getenv("AUTH_SECRET_42"),
    }

    return render(request, "login.html", context)

    # ? STEP 2 : get either access or not
    # ? STEP 3.1 : USER REFUSES ACCESS
    # => Refuses access redirects him towrads the login page
    # ? STEP 3.2 : USER GRANT ACCESS
    # => Get the token back and store it
    # ! WE CAN STORE THE GIVEN TOKEN IN A JWT
    # ? STEP 3.2 :
    # ? STEP 1 :
    # ? STEP 1 :
    # ? STEP 1 :
    # ? STEP 1 :
    # ? STEP 1 :
    # ? STEP 1 :
    # ? STEP 1 :
