import threading
import time
import match_app.services.consumer as consumer
import asyncio
import json
import aiohttp
from enum import Enum
import math

class State(Enum):
	waiting = "waiting"
	running = "running"
	end = "end"

class Pong:

	id = 0
	def __init__(self, idP1, idP2):
		# pongs.append(self)
		Pong.id += 1
		self.id = Pong.id
		self.idP1 = idP1
		self.idP2 = idP2
		self.pad_height = 40
		self.yp1 = self.pad_height / 2
		self.yp2 = self.pad_height / 2
		self.pad_width = 10
		self.winner = None
		self.max_delay = 900
		self.send_task = None
		self.watch_task = None
		self.ball = [50, 50]
		self.vect = [1 / math.sqrt(2), 1 / math.sqrt(2)]
		self.score = [0, 0]
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

		if playerId in (self.idP1, self.idP2): 	
			# self.sendTask.cancel()
			# try:
			# 	await self.sendTask  # Attendre que l'annulation soit complète
			# except asyncio.CancelledError:
			# 	print("Tâche annulée avec succès")	 
			self.state = State.end
			if self.winner is None and self.start_flag:
				self.winner = self.idP1	if playerId == self.idP2 \
					else self.idP2
			if self.winner is None and not self.start_flag:
				self.winner = self.idP1	if playerId == self.idP2 \
					else self.idP2
			# asyncio.run_coroutine_threadsafe(self.stop_tasks, self.myEventLoop)
			await self.sendFinalState()
			return True
		return False

	async def stop_tasks(self):

		tasks = [self.send_task, self.watch_task]
		for task in tasks:
			if task and not task.done() and not task.cancelled():
				task.cancel()
		await asyncio.gather(*[t for t in tasks if t], return_exceptions=True)

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
		try:
			self.myEventLoop.run_until_complete(self.launch())  
		finally:			
			tasks = [
				t for t in asyncio.all_tasks(self.myEventLoop) if not t.done()]
			for task in tasks:
				task.cancel()
			self.myEventLoop.run_until_complete(
				asyncio.gather(*tasks, return_exceptions=True))
			self.myEventLoop.stop()
			self.myEventLoop.close()
			print(f"Event loop fermé proprement pour match {self.id}", flush=True)

	# def launchTask(self):
	# 	self.start_flag = False
	# 	self.myEventLoop = asyncio.new_event_loop()
	# 	asyncio.set_event_loop(self.myEventLoop)
	# 	self.myEventLoop.create_task(self.launch())
	# 	# self.myEventLoop.run_forever()
	# 	# myEventLoop.run_until_complete(asyncio.Future())
	# 	self.myEventLoop.run_until_complete(self.launch())
	
	# 	self.myEventLoop.stop()
	# 	self.myEventLoop.close() 
	# 	print("in match after RUN", flush=True)

	async def launch(self):
		self.state = State.waiting
		# self.sendTask = self.myEventLoop.create_task(self.sendState())
		self.send_task = self.myEventLoop.create_task(self.sendState())
		self.watch_task = self.myEventLoop.create_task(self.watch_dog())
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
						if self.yp1 >= (self.pad_height / 2) + 2:
							self.yp1 -= 2
					elif self.player1["dir"] == 'down':
						if self.yp1 <= 100 - (self.pad_height / 2) - 2:
							self.yp1 += 2
					self.player1["dir"] = None
				if  self.player2.get("dir") is not None :
					if self.player2["dir"] == 'up':
						if self.yp2 >= (self.pad_height / 2) + 2:							
							self.yp2 -= 2
					elif self.player2["dir"] == 'down':
						if self.yp2 <= 100 - (self.pad_height / 2) - 2:
							self.yp2 += 2
					self.player2["dir"] = None

				self.ball[0] += self.vect[0]				
				self.ball[1] += self.vect[1]
			
				# if self.ball[0] >= 100:
				# 	self.vect[0] = -self.vect[0]
				# if self.ball[0] == 0 :
				# 	self.vect[0] = -self.vect[0]

# bord haut et bas
				if self.ball[1] >= 98:
					self.vect[1] = -self.vect[1]
					self.ball[1] = 98
				if self.ball[1] <= 0 :
					self.ball[1] = 0
					self.vect[1] = -self.vect[1]

				# if self.ball[1] > 100:
				# 	self.ball[1] = 99
				# if self.ball[1] < 0:
				# 	self.ball[1] = 1

# bord droit et gauche
				if self.ball[0] >= 100:
					self.score[1] += 1
					self.ball = [50, 50]
					self.vect = [1 / math.sqrt(2), 1 / math.sqrt(2)]
				if self.ball[0] <= 0:
					self.score[0] += 1
					self.ball = [50, 50]
					self.vect = [1 / math.sqrt(2), 1 / math.sqrt(2)]

				# if self.ball[0] == 1 and self.ball[1] >= self.yp1 and self.ball[1] <= self.yp1 + 10 \
				# 	or self.ball[0] == 89 and self.ball[1] == self.yp2:
				# 		self.vect[0] = -self.vect[0]
				
				# if self.ball[0] == 1 and self.yp1 <= self.ball[1] <= self.yp1 + 10 \
				# or self.ball[0] == 89 and self.yp2 <= self.ball[1] <= self.yp2 + 10:
				# 	self.vect[0] = -self.vect[0]
				
				if (self.ball[0] <= 15) and \
					(self.yp1 - (self.pad_height / 2) <= self.ball[1] <= self.yp1 + (self.pad_height / 2)):
					
					new_vect = [0, 0]
					new_vect[0] = 15 - self.ball[0]
					new_vect[1] = self.cross_product(self.vect[0], self.vect[1], new_vect[0])
					self.ball[0] += new_vect[0]				
					self.ball[1] += new_vect[1]
					await asyncio.sleep(0.05)
					# self.vect[0] = -self.vect[0]
					# y = (self.ball[1] - self.yp1) / 20
					# print(f"selfY 222: {self.vect[1]}", flush=True)
					# print(f"selfX 222: {self.vect[0]}", flush=True)
					sub_vect = self.substract_vect(self.vect, new_vect)

					tmp = sub_vect[0]
					y = (self.ball[1] - self.yp1) / (self.pad_height / 2) 
					x = (sub_vect[0] ** 2) + (sub_vect[1] ** 2) - (y ** 2)
					x = math.sqrt(x)
					if tmp > 0:
						x = -x
					self.ball[0] += x			
					self.ball[1] += y
					await asyncio.sleep(0.05)
					self.vect[0] = -self.vect[0] + 0.5
					self.vect[1] = self.vect[1] + 0.5
					# tmp = self.vect[0]
					# y = (self.ball[1] - self.yp1) / (self.pad_height / 2) 
					# x = (self.vect[0] ** 2) + (self.vect[1] ** 2) - (y ** 2)
					# x = math.sqrt(x)
					# if tmp > 0:
					# 	x = -x

					print(f"Y 222: {y}", flush=True)
					print(f"X 222: {x}", flush=True)
					# print(f"Y 222: {y}", flush=True)
					# print(f"VECT: {self.vect[1]}", flush=True)
					# self.vect[0] = x + 0.5
					# self.vect[1] = y + 0.5
					# print(f"VECT222: {self.vect[1]}", flush=True)
				
				if  (self.ball[0] >= 83) and \
						(self.yp2 - (self.pad_height / 2) <= self.ball[1] <= self.yp2 + (self.pad_height / 2)):
				
					print(f"selfY 222: {self.vect[1]}", flush=True)
					print(f"selfX 222: {self.vect[0]}", flush=True)
					# self.vect[0] = -self.vect[0]
					tmp = self.vect[0]
					y = (self.ball[1] - self.yp2) / (self.pad_height / 2) 
					
					print(f"Y: {y}", flush=True)
					x = (self.vect[0] ** 2) + (self.vect[1] ** 2) - (y ** 2)
					x = math.sqrt(x)
					if tmp > 0:
						x = -x
					# else
					# 	x = -x
		
					print(f"Y 222: {y}", flush=True)
					print(f"X 222: {x}", flush=True)
					# print(f"VECT: {self.vect[1]}", flush=True)
					self.vect[0] = x
					self.vect[1] = y
					# print(f"VECT222: {self.vect[1]}", flush=True)
			else:
				if self.start_flag:
					if self.player1:
						self.winner = self.idP1 
					elif self.player2:
						self.winner = self.idP2
				self.state = State.waiting
				# print(f"je suis en waiting", flush=True)

			
				# self.sendTask.cancel()
				# try:
				# 	await self.sendTask  # Attendre que l'annulation soit complète
				# except asyncio.CancelledError:
				# 	print("Tâche annulée avec succès")		
				
			if 10 == self.score[0]:
				self.winner = self.idP1
				self.state = State.end
				await self.sendFinalState()
			if 10 == self.score[1]:
				self.winner = self.idP2
				self.state = State.end
				await self.sendFinalState()
				# self.sendTask.cancel()
				# try:
				# 	await self.sendTask  # Attendre que l'annulation soit complète
				# except asyncio.CancelledError:
				# 	print("Tâche annulée avec succès")
				# self.winner = self.idP2
				# self.state = State.end
				# await self.sendFinalState()	

			# print(f"ACTUAL WINNER:{self.winner}", flush=True)
			await asyncio.sleep(0.05)
		# self.stop_tasks()
		# tasks = [self.send_task, self.watch_task]
		# for task in tasks:
		# 	if task and not task.done() and not task.cancelled():
		# 		task.cancel()
		# await asyncio.gather(
		# 	*[t for t in tasks if t], return_exceptions=True)
		print(f"in match after WHILE id:{self.id}", flush=True)

	def cross_product(self, x, y, nx):
		return nx * y / x
	
	def substract_vect(self, vect_a, vect_b):
		new_vect = [0, 0]
		new_vect[0] = vect_a[0] - vect_b[0]
		new_vect[1] = vect_a[1] - vect_b[1]
		return new_vect
	
	async def watch_dog(self):
		delay = 0
		while self.state != State.end:			
			if self.state == State.running:
				delay = 0
			if (delay > self.max_delay):
				print(f"stopped by wathdog", flush=True)
				await self.stop(self.idP1)
				return
			delay += 1
			await asyncio.sleep(1.00)

	async def sendState(self):		
		while self.state != State.end:	
			self.myplayers = [p for p in consumer.players
				if self.id == p["matchId"]]
			for p in self.myplayers:
				state = self.state
				if state != State.end:
					try:												
						await p["socket"].send(text_data=json.dumps({
							"state": state.name,
							"yp1": self.yp1,
							"yp2": self.yp2,
							"ball": self.ball,
							"score": self.score
						}))                  
					except Exception as e:
						pass				
			await asyncio.sleep(0.05)

	async def sendFinalState(self):				
		self.myplayers = [p for p in consumer.players
			if self.id == p["matchId"]]
		for p in self.myplayers:
			try:					
				await p["socket"].send(text_data=json.dumps({
				"state": self.state.name,
				"winnerId": self.winner,
				"score": self.score
				}))
			except Exception as e:
				pass		
	
		async with aiohttp.ClientSession() as session:
			async with session.post(
				"http://tournament:8001/tournament/match-result/", json={
				"matchId": self.id,
				"winnerId": self.winner,
				"looserId": self.idP1 if self.winner == self.idP2
					else self.idP2,
				"p1Id": self.idP1,
				"p2Id": self.idP2,
				"score": self.score
			}) as response:
				if response.status != 200 and response.status != 201:
					err = await response.text()
					print(f"Erreur HTTP {response.status}: {err}", flush=True)
		from match_app.views import del_pong
		del_pong(self.id)			
