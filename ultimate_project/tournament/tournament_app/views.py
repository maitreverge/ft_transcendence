from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import requests
# Create your views here.
from django.http import JsonResponse

def test(request):
    return render(request, "test.html", {"touille": "champion du bidule"})

class User:
	def __init__(self, id):
		self.id = id
tournamentUsers = [User(1), User(2)]

def start_tournament(request : HttpRequest):	
	return render(request, "selections.html", {"tournamentUsers": tournamentUsers})


def start_match(request):
	select = request.GET.get("select_id")
	data = requests.get("http://ctn-match:8002/match/new-match/").json() #! opti url and gateway!
	print(data, flush=True)
	# return JsonResponse(data, status= 201)
	return render(request, "test.html", {"matchData": data})