import os
from django.shortcuts import render
from django.http import HttpRequest
from django.template import Context, Template

def profile(request : HttpRequest):	
	return render(
		request,
		"profile.html",
		{
			"rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),			
		}
	)
