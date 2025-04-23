import os
from django.shortcuts import render
from match_app.services.pong import Pong
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse, JsonResponse

pongs = []

def new_match(request: HttpRequest):
    
	multy = request.GET.get("multy")
	multy = True if multy == 'True' else False 
	p1 = (int(request.GET.get("p1Id")), request.GET.get("p1Name"))
	p2 = (int(request.GET.get("p2Id")), request.GET.get("p2Name"))
	mode = request.GET.get("m")
	pong = Pong(multy, p1, p2, mode)
	pongs.append(pong)
	return JsonResponse({"matchId": pong.id}, status=201)

def safe_int(value, default=0):

	try:
		return int(value)
	except (TypeError, ValueError) as e:
		print(e)
		return default

def enter_match2d(request: HttpRequest):
    
	client_host = request.get_host().split(":")[0]

	if client_host in ["127.0.0.1", "localhost"]:
		pidom = "localhost:8443"
	else:
		pidom = os.getenv("HOST_IP", "localhost:8443")
	print("ICIIIIIIIIII", flush=True)
	print(f"{safe_int(request.GET.get('playerId', '0'))}, "
		f"{request.GET.get('playerName', '0')}, "
		f"{safe_int(request.GET.get('player2Id', '0'))}, "
		f"{request.GET.get('player2Name', '0')}",
		flush=True)

	return render(
		request,
		"pong2d.html",
		{
			"pidom": os.getenv("HOST_IP", "localhost:8443"),
			"matchId": safe_int(request.GET.get("matchId", "0")),
			"playerId": safe_int(request.GET.get("playerId", "0")),
			"playerName": request.GET.get("playerName", "0"),
			"player2Id": safe_int(request.GET.get("player2Id", "0")),
			"player2Name": request.GET.get("player2Name", "0"),
		},
	)

def enter_match3d(request: HttpRequest):

	client_host = request.get_host().split(":")[0]

	if client_host in ["127.0.0.1", "localhost"]:
		pidom = "localhost:8443"
	else:
		pidom = os.getenv("HOST_IP", "localhost:8443")

	return render(
		request,
		"pong3d.html",
		{
			"pidom": os.getenv("HOST_IP", "localhost:8443"),
			"matchId": safe_int(request.GET.get("matchId", "0")),
			"playerId": safe_int(request.GET.get("playerId", "0")),
			"playerName": request.GET.get("playerName", "0"),
			"player2Id": safe_int(request.GET.get("player2Id", "0")),
			"player2Name": request.GET.get("player2Name", "0"),
		},
	)

async def stop_match(request: HttpRequest, playerId, matchId):

	print(f"STOP MATCH pid: {playerId}, mid: {matchId}", flush=True)
	match_id = safe_int(matchId)
	player_id = safe_int(playerId)
	if all((match_id , player_id)): 
		for p in pongs:
			if p.id == match_id:
				if await p.stop(player_id):
					return JsonResponse({"status": "succes"})
				else:
					return JsonResponse({"status": "fail"}, status=400)
	return JsonResponse({"status": "not authorized"}, status=400)

def is_in_match(request: HttpRequest):

	print(f"\033[31mIS IN MATCH pid: {request.GET.get('playerId')}\033[0m", flush=True)

	player_id = request.GET.get('playerId')	
	player_id = safe_int(player_id)
	if player_id:
		pong = next(
			(p for p in pongs if any(
				plyId == player_id and p.mode == 's'
				for plyId in getattr(p, 'plyIds', [])
			))
		, None)
		if pong:
			print(f"\033[31m TRUE\033[0m", flush=True)	
			return JsonResponse({"p1": pong.plyIds[0], "p2": pong.plyIds[1]})	
	print(f"\033[31m PAS TRUE\033[0m", flush=True)	
	return JsonResponse({'p1': False, 'p2': False})
	
def del_pong(pong_id):

	print(f"DEL PONG {pong_id}", flush=True)
	from match_app.services.match_consumer import players
		
	pong = next((p for p in pongs if p.id == pong_id), None)
	print(players, flush=True)
	print(pongs, flush=True)
	print("c la mouquate pongs.players", flush=True)
	# print(pong.users, flush=True)
	if pong: 
		players[:] = [
			p for p in players if not any(
				p['playerId'] == po['playerId'] for po in pong.users   
		)]	
		pongs[:] = [p for p in pongs if p.id != pong_id]
	print(players, flush=True)
	print(pongs, flush=True)
