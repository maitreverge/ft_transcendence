import os
import json
import tournament_app.services.simple_match_consumer as sm_cons
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tournament_app.services.tournament_consumer import tournaments


def simple_match(request: HttpRequest, user_id):
    print(f"dans simple match {user_id}", flush=True)
    return render(
        request,
        "simple_match.html",
        {
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8443"),
            "user_id": user_id,
            # "username": request.headers.get("X-Username"),
        },
    )


@csrf_exempt
async def match_players_update(request: HttpRequest):
    print(f"MATCH PLAYERS UPDATE VIEWS", flush=True)
    data = json.loads(request.body.decode("utf-8"))
    match_id = data.get("matchId", None)
    players = data.get("players", [])
    match = next((m for m in sm_cons.matchs if m.get("matchId") == match_id), None)
    if match:
        match["players"] = players
        await sm_cons.SimpleConsumer.match_update()
    tournament = next(
        (
            t
            for t in tournaments
            if any(data.get("matchId") == m.get("matchId") for m in t.matchs)
        ),
        None,
    )
    if tournament:
        await tournament.match_players_update(data)

    return JsonResponse({"status": "succes"})


@csrf_exempt
async def match_result(request: HttpRequest):
    print("MATCH RESULT", flush=True)
    data = json.loads(request.body.decode("utf-8"))
    match_id = data.get("matchId")
    winner_id = data.get("winnerId")
    looser_id = data.get("looserId")
    p1_id = data.get("p1Id")
    p2_id = data.get("p2Id")
    p1 = next((p for p in sm_cons.players if p.get("playerId") == p1_id), None)
    p2 = next((p for p in sm_cons.players if p.get("playerId") == p2_id), None)
    if p1:
        p1["busy"] = None
    if p2:
        p2["busy"] = None
    print(f"MATCH BEFORE RM match_id:{match_id} matchs: {sm_cons.matchs}", flush=True)
    sm_cons.matchs[:] = [m for m in sm_cons.matchs if m.get("matchId") != match_id]
    print(f"MATCH AFTER RM {sm_cons.matchs}", flush=True)
    await sm_cons.SimpleConsumer.match_update()

    tournament = next(
        (
            t
            for t in tournaments
            if any(match_id == m.get("matchId", None) for m in t.matchs)
        ),
        None,
    )
    if tournament:
        await tournament.match_result(match_id, winner_id, looser_id)
    return JsonResponse({"status": "succes"})


def tournament(request: HttpRequest, user_id):
    print(f"dans tournament {user_id}", flush=True)  # //!
    return render(
        request,
        "tournament.html",
        {
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8443"),
            "user_id": user_id,
            # "username": request.headers.get("X-Username"),
        },
    )


def tournament_pattern(request: HttpRequest, tournament_id):
    print(f"dans tournament pattern {tournament_id}", flush=True)
    return render(
        request,
        "tournament_pattern.html",
    )


# def create_tournament(playerList):
# 	player1
# 	player2
# 	player3
# 	player4
# 	askmatchid
# 	send matchid to player1 player2
# 	send matchid to player3 player4

# 	makegamewith player1 player2 les joueur vont se connecter
# 	makegamewith player3 player4 les joueur vont se connecter

# 	winnergame1 je vais recevoir le res par match result
# 	winnergame2	je vais recevoir le res par match result
# 	une fois que les deux res sont arrive je vais
# 	askmatchId
# 	send matchid to winnergame1 winnergame2

# 	makegamewith winnergame1 winnergame2

# 	winnergame1 je vais recevoir le res par match result
# 	winnergame3
