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
		}
	)

@csrf_exempt
async def match_result(request : HttpRequest):	
	result = json.loads(request.body.decode('utf-8'))
	match_id = result.get('matchId')
	winner_id = result.get('winnerId')
	looser_id = result.get('looserId')
	p1_id = result.get('p1Id')
	p2_id = result.get('p2Id')
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
	