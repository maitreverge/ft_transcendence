from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import requests
# Create your views here.
from django.http import JsonResponse
import os

import tournament_app.services.consumer as consumer

def test(request):
    return render(request, "test.html", {"touille": "champion du bidule"})

class User:
	def __init__(self, id):
		self.id = id
tournamentUsers = [User(1), User(2)]
simpleUsers = []

def start_tournament(request : HttpRequest):	
	simpleUsers.append(User(len(simpleUsers)))	
	return render(request, "selections.html", {"tournamentUsers": tournamentUsers})

def receive_invit(request):
	p1 = request.GET.get('select')

matchs = []
def start_match(request):
	# p1 =consumer.players[''].id
	matchId = request.GET.get('matchId', None)
	print(f"first print matchId in start match: {matchId}", flush=True)
	if matchId is None:
		p1 = request.GET.get('selfid')
		p2 = request.GET.get('select')
		# print(f"select:{select}", flush=True)
		data = requests.get(f"http://ctn-match:8002/match/new-match/?p1={p1}&p2={p2}").json() #! opti url and gateway!!!
		matchs.append({"matchId": data, "playerId": p2, "otherId": p1})
		print(data, flush=True)
		return render(request, "test.html", {"matchData": data, "playerId": p1, "otherId": p2})
	else:
		print(f"matchId in start match: {matchId}", flush=True)
		for p in matchs:
			print(p, flush=True)
		choosenMatch = [p for p in matchs if p['matchId']['id'] == matchId]	
		print("choosenMatch: ", flush=True)
		print(choosenMatch, flush=True)
		return render(request, "test.html", {"matchData": choosenMatch[0]['matchId'], "playerId": choosenMatch[0]['playerId'], "otherId": choosenMatch[0]['otherId']})
	# return JsonResponse(data, status= 201)
	

def simple_match(request : HttpRequest):	

	return render(request, "selections-simple.html", {"rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"), "simpleUsers": consumer.players})