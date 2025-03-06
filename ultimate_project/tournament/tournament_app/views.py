import os
import json
import tournament_app.services.consumer as consumer
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def simple_match(request : HttpRequest, user_id):
	print(f"dans simple match {user_id}", flush=True)	
	return render(
		request,
		"selection_simple.html",
		{
			"rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),	
			"user_id": user_id		
		}
	)

@csrf_exempt
async def match_players_update(request : HttpRequest):
	data = json.loads(request.body.decode('utf-8'))
	match_id = data.get('matchId', None)
	players = data.get('players', [])
	match = next(
		(m for m in consumer.matchs if m.get("matchId" == match_id)), None)
	match.append(players)
@csrf_exempt
async def match_result(request : HttpRequest):	
	data = json.loads(request.body.decode('utf-8'))
	match_id =	data.get('matchId')
	winner_id =	data.get('winnerId')
	looser_id =	data.get('looserId')
	p1_id =	data.get('p1Id')
	p2_id =	data.get('p2Id')
	p1 = next((p for p in consumer.players if p.get('playerId') == p1_id), None)
	p2 = next((p for p in consumer.players if p.get('playerId') == p2_id), None)
	if p1:
		p1['busy'] = None
	if p2:
		p2['busy'] = None
	consumer.matchs[:] = [m for m in consumer.matchs
		if m.get("matchId") != match_id]
	await consumer.MyConsumer.match_update()
	return JsonResponse({"status": "succes"})
	
