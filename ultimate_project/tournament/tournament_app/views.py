from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import requests
# Create your views here.
from django.http import JsonResponse
import os

import tournament_app.services.consumer as consumer

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

async def start_match(request):
	# p1 =consumer.players[''].id
	matchId = request.GET.get('matchId', None)
	print(f"first print matchId in start match: {matchId}", flush=True)
	if matchId is None:
		p1 = request.GET.get('selfid')
		p2 = request.GET.get('select')
		# print(f"select:{select}", flush=True)
		newMatchId = requests.get(f"http://match:8002/match/new-match/?p1={p1}&p2={p2}").json()['matchId'] #! opti url and gateway!!!
		consumer.matchs.append({"matchId": newMatchId, "playerId": p2, "otherId": p1})
		await consumer.MyConsumer.matchUpdate()
		print(newMatchId, flush=True)
		return JsonResponse({"matchId": newMatchId}, status= 201)
		return render(request, "match_simple.html", {"matchId": newMatchId, "playerId": p1, "otherId": p2})
	else:
		for p in consumer.matchs:
			print(p, flush=True)
		choosenMatch = [p for p in consumer.matchs if p['matchId'] == matchId]	
		print("choosenMatch: ", flush=True)
		print(choosenMatch, flush=True)
		return render(request, "match_simple.html", {"matchId": choosenMatch[0]['matchId'], "playerId": choosenMatch[0]['playerId'], "otherId": choosenMatch[0]['otherId']})
	# return JsonResponse(matchId, status= 201)
	

def simple_match(request : HttpRequest):	

	return render(request, "selection_simple.html", {"rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"), "simpleUsers": consumer.players})