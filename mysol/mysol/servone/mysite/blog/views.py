from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests
# Create your views here.

# def home(request):
#     return HttpResponse("salut monde")

def home(request):
    return render(request, 'blog/salut.html')

def callservtwo(request):
	try:
		data = requests.get("http://mysite2:8001/blog2/").json()
		return JsonResponse({"service2_resp": data})
	except requests.exceptions.RequestException as e:
		return JsonResponse({"error": str(e)}, status=500)
	
    