import requests
import os
import json
import tournament_app.services.consumer as consumer
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def simple_match(request : HttpRequest):	
	return render(
		request,
		"selection_simple.html",
		{
			"rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),
			"simpleUsers": consumer.players
		}
	)
	
async def start_match(request):
	p1 = request.GET.get('selfid')
	p2 = request.GET.get('select')
	newMatchId = requests.get(
		f"http://match:8002/match/new-match/?p1={p1}&p2={p2}"
	).json()['matchId']
	consumer.matchs.append({
		"matchId": newMatchId,
		"playerId": p2, 
		"otherId": p1
	})
	await consumer.MyConsumer.matchUpdate()
	return JsonResponse({"matchId": newMatchId}, status= 201)

@csrf_exempt
async def match_result(request : HttpRequest):	
	result = json.loads(request.body.decode('utf-8'))
	matchId = result.get('matchId')
	winner = result.get('winnerId')
	consumer.matchs[:] = [m for m in consumer.matchs
		if m.get("matchId") == matchId]
	await consumer.MyConsumer.matchUpdate()
	return JsonResponse({"status": "succes"})
	