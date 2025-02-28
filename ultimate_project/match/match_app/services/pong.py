import threading
import time
import match_app.services.consumer as consumer
import asyncio
import json
import requests
from enum import Enum

class State(Enum):
	waiting = "waiting"
	running = "running"
	end = "end"

class Pong:

	id = 0
	def __init__(self, idP1, idP2):
		Pong.id += 1
		self.id = Pong.id
		self.idP1 = idP1
		self.idP2 = idP2
		self.yp1 = 0
		self.yp2 = 0
		self.winner = None

		# asyncio.run(self.end())
		threading.Thread(target=self.launchTask, daemon=True).start()

	# async def end(self):
	# 	print("end un", flush=True)
	# 	await self.two()
	# 	print("end deux", flush=True)
		
	# async def two(self):
	# 	print("two un", flush=True)
	# 	await self.three()
	# 	print("two deux", flush=True)
		
	# async def three(self):
	# 	print("three un", flush=True)
	# 	await asyncio.sleep(1)
	# 	print("three deux", flush=True)

	async def stop(self, playerId):
		print(f"in stop PONG my id is : {self.id}", flush=True)
		if str(playerId) in (self.idP1, self.idP2): 	
			self.state = State.end
			if self.winner is None and self.start_flag:
				self.winner = self.idP1	if str(playerId) == self.idP2 \
					else self.idP2 
			await self.sendFinalState()
			return True
		return False

	# def stop(self, playerId):
	# 	print(f"in stop PONG my id is : {self.id}", flush=True)
	# 	print(f"self.idP1: {self.idP1}, self.idP2: {self.idP2}, playerId: {playerId}", flush=True)

	# 	if playerId in (self.idP1, self.idP2):
	# 		print("Player is authorized to stop the match", flush=True)
	# 		self.state = State.end
	# 		print(f"Match {self.id} state updated to {self.state}", flush=True)
	# 		return True

	# 	print("Player not authorized to stop the match", flush=True)
	# 	return False

	def launchTask(self):
		self.start_flag = False
		self.myEventLoop = asyncio.new_event_loop()
		asyncio.set_event_loop(self.myEventLoop)
		self.myEventLoop.create_task(self.launch())
		# self.myEventLoop.run_forever()
		# myEventLoop.run_until_complete(asyncio.Future())
		self.myEventLoop.run_until_complete(self.launch())
		print("in match after RUN", flush=True)

	async def launch(self):
		self.state = State.waiting
		self.myEventLoop.create_task(self.sendState())
		while self.state in (State.running, State.waiting):		
		
			self.myplayers = [p for p in consumer.players
				if self.id == p["matchId"]]
			self.player1 = next(
				(p for p in self.myplayers if self.idP1 == p["playerId"]), None)
			self.player2 = next(
				(p for p in self.myplayers if self.idP2 == p["playerId"]), None)

			if None not in (self.player1, self.player2):
				self.winner = None
				self.start_flag = True
				self.state = State.running
				if self.player1.get("dir") is not None :
					if self.player1["dir"] == 'up':
						self.yp1 -= 1
					elif self.player1["dir"] == 'down':
						self.yp1 += 1
					self.player1["dir"] = None
				if  self.player2.get("dir") is not None :
					if self.player2["dir"] == 'up':
						self.yp2 -= 1
					elif self.player2["dir"] == 'down':
						self.yp2 += 1
					self.player2["dir"] = None
			else:
				if self.start_flag:
					if self.player1:
						self.winner = self.idP1 
					elif self.player2:
						self.winner = self.idP2
				self.state = State.waiting
				# print(f"je suis en waiting", flush=True)

			if self.yp1 > 80:		
				self.winner = self.idP1
				self.state = State.end
				await self.sendFinalState()
			elif self.yp2 > 80:
				self.winner = self.idP2
				self.state = State.end
				await self.sendFinalState()	
			# print(f"ACTUAL WINNER:{self.winner}", flush=True)
			await asyncio.sleep(0.05)
		print(f"in match after WHILE id:{self.id}", flush=True)

	async def sendState(self):		
		while (True):	
			self.myplayers = [p for p in consumer.players
				if self.id == p["matchId"]]
			for p in self.myplayers:	
				await p["socket"].send(text_data=json.dumps({
					"state": self.state.name,
					"yp1": self.yp1,
					"yp2": self.yp2
				}))
			await asyncio.sleep(0.05)

	async def sendFinalState(self):				
		self.myplayers = [p for p in consumer.players
			if self.id == p["matchId"]]
		for p in self.myplayers:	
			await p["socket"].send(text_data=json.dumps({
				"state": self.state.name,
				"winnerId": self.winner
			}))
		requests.post("http://tournament:8001/tournament/match-result/", json={
			"matchId": self.id,
			"winnerId": self.winner
		})
	