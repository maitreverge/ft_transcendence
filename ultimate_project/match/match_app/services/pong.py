import threading
import time
import match_app.services.consumer as consumer
import asyncio
import json
import aiohttp
from enum import Enum
import math
import requests
import operator as op

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
		# self.idP1 = idP1
		# self.idP2 = idP2
		self.plyIds = [idP1, idP2]
		self.pad_height = 40
	
		# self.pads_y[0]
		self.pads_y = [self.pad_height / 2, self.pad_height / 2]
		self.pad_width = 10
		self.winner = None
		self.max_delay = 15
		self.send_task = None
		self.watch_task = None
		self.ball_rst = [25, 5]
		self.ball = self.ball_rst.copy()
		self.vect_rst = [1, 1]
		self.vect = self.vect_rst.copy()
		self.score = [0, 0]
		self.mag = None
		self.has_wall = False
		self.pad_speed = 4
		self.max_speed = 10
		self.acceleration = 1.1
		self.max_score = 5
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

		if playerId in self.plyIds: 	
			print(f"le player est bien autorise a fermer le match", flush=True)
			# self.sendTask.cancel()
			# try:
			# 	await self.sendTask  # Attendre que l'annulation soit complète
			# except asyncio.CancelledError:
			# 	print("Tâche annulée avec succès")	 
			self.state = State.end
			if self.winner is None and self.start_flag:
				self.winner = self.plyIds[0] \
					if playerId == self.plyIds[1] else self.plyIds[1]
			if self.winner is None and not self.start_flag:
				self.winner = self.plyIds[0] \
					if playerId == self.plyIds[1] else self.plyIds[1]
			# asyncio.run_coroutine_threadsafe(self.stop_tasks, self.myEventLoop)
			await self.sendFinalState()
			return True
		print(f"le player n'est pas bien autorise a fermer le match", flush=True)
		return False

	# async def stop_tasks(self):

	# 	tasks = [self.send_task, self.watch_task]
	# 	for task in tasks:
	# 		if task and not task.done() and not task.cancelled():
	# 			task.cancel()
	# 	await asyncio.gather(*[t for t in tasks if t], return_exceptions=True)

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
			self.myEventLoop.create_task(self.launch_game())
			self.myEventLoop.run_forever()
			# self.myEventLoop.run_until_complete(self.launch())  
		finally:
			time.sleep(2)			
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



	# def applyPadsCommands(self, player, pad_y):

	# 	if self.player1.get("dir") is not None :
	# 		if self.player1["dir"] == 'up':					
	# 			self.pads_y[0] = max(
	# 				self.pads_y[0] - self.pad_speed,
	# 				(self.pad_height / 2)
	# 			)							
	# 		elif self.player1["dir"] == 'down':					
	# 			self.pads_y[0] = min(
	# 				self.pads_y[0] + self.pad_speed,
	# 				100 - (self.pad_height / 2)
	# 			)					
	# 		self.player1["dir"] = None
	# 	if self.player2.get("dir") is not None :
	# 		if self.player2["dir"] == 'up':
	# 			self.pads_y[1] = max(
	# 				self.pads_y[1] - self.pad_speed,
	# 				(self.pad_height / 2)
	# 			)						
	# 		elif self.player2["dir"] == 'down':
	# 			self.pads_y[1] = min(
	# 				self.pads_y[1] + self.pad_speed,
	# 				 100 - (self.pad_height / 2)
	# 			)					
	# 		self.player2["dir"] = None

	def applyPadCommand(self, player, pad_index):

		if player.get("dir") is not None :
			if player["dir"] == 'up':					
				self.pads_y[pad_index] = max(
					self.pads_y[pad_index] - self.pad_speed,
					(self.pad_height / 2)
				)							
			elif player["dir"] == 'down':					
				self.pads_y[pad_index] = min(
					self.pads_y[pad_index] + self.pad_speed,
					100 - (self.pad_height / 2)
				)					
			player["dir"] = None

	async def score_point(self, cmp, limit, score_index):

		if cmp(self.ball[0], limit):
			self.score[score_index] += 1
			self.ball = self.ball_rst.copy()
			self.vect = self.vect_rst.copy()
			await asyncio.sleep(1)

	async def max_score_rise(self, ply_index):
		
		if self.max_score == self.score[ply_index]: 
			self.winner = self.plyIds[ply_index]
			self.state = State.end
			await self.sendFinalState()
	
	async def horz_bounce(self, cmp, limit, pad_y_index, dir):
		# if ((self.ball[0] + self.vect[0]) <= 16) and \
		# 	self.segments_intersect((self.ball[0], self.ball[1]), (self.ball[0] + self.vect[0], self.ball[1] + self.vect[1]), (16, self.pads_y[0] - (self.pad_height / 2)), (16, self.pads_y[0] + (self.pad_height / 2))):
		if self.is_pad_intersecting(cmp, limit, pad_y_index):			
			new_vect = [0, 0]
			new_vect[0] = limit - self.ball[0]
			new_vect[1] = self.scale_vector(new_vect[0], self.vect[1], self.vect[0])
			self.ball[0] += new_vect[0]				
			self.ball[1] += new_vect[1]
			self.has_wall = True
			await asyncio.sleep(0.05)				
	
			mag = self.get_magnitude(self.vect) 				
			y = (self.ball[1] - self.pads_y[pad_y_index]) / (self.pad_height / 2) 
			y = y * mag
			y = max(min(y, 0.9), -0.9)
			x = (self.vect[0] ** 2) + (self.vect[1] ** 2) - (y ** 2)								
			x = math.sqrt(abs(x))	

			scl = 1
			if abs(self.vect[0]) < self.max_speed and abs(self.vect[1]) < self.max_speed:
				scl = self.acceleration
			self.vect[0] = scl * x * dir
			self.vect[1] = scl * y 
		
			self.flag = False

	async def launch_game(self):
		self.state = State.waiting
		# self.sendTask = self.myEventLoop.create_task(self.sendState())
		self.send_task = self.myEventLoop.create_task(self.sendState())
		self.watch_task = self.myEventLoop.create_task(self.watch_dog())
		while self.state in (State.running, State.waiting):		
			self.has_wall = False
			self.flag = True
			self.myplayers = [p for p in consumer.players
				if self.id == p["matchId"]]
			self.player1 = next(
				(p for p in self.myplayers if self.plyIds[0] == p["playerId"]), None)
			self.player2 = next(
				(p for p in self.myplayers if self.plyIds[1] == p["playerId"]), None)

			if None not in (self.player1, self.player2):
			
				self.winner = None
				self.start_flag = True
				self.state = State.running

				self.applyPadCommand(self.player1, pad_index=0)
				self.applyPadCommand(self.player2, pad_index=1)			

				await self.score_point(op.ge, limit=100, score_index=0)
				await self.score_point(op.le, limit=0, score_index=1)
				await self.max_score_rise(ply_index=0)
				await self.max_score_rise(ply_index=1)
				await self.horz_bounce(op.le, limit=16, pad_y_index=0, dir=+1)
				await self.horz_bounce(op.ge, limit=84, pad_y_index=1, dir=-1)
				await self.vert_bounce(op.le, limit=1)
				await self.vert_bounce(op.ge, limit=99)
				# if ((self.ball[0] + self.vect[0]) <= 16) and \
				# 	self.segments_intersect((self.ball[0], self.ball[1]), (self.ball[0] + self.vect[0], self.ball[1] + self.vect[1]), (16, self.pads_y[0] - (self.pad_height / 2)), (16, self.pads_y[0] + (self.pad_height / 2))):

				# 	# (self.pads_y[0] - (self.pad_height / 2) <= self.ball[1] + self.vect[1] <= self.pads_y[0] + (self.pad_height / 2)):
				
				# 	new_vect = [0, 0]
				# 	new_vect[0] = 16 - self.ball[0]
				# 	new_vect[1] = self.scale_vector(new_vect[0], self.vect[1], self.vect[0])

				# 	# if (not self.get_top_bounce_vect(0) or self.get_magnitude(new_vect) < self.get_magnitude(self.get_top_bounce_vect(0))) and \
		 		# 	# 	(not self.get_bot_bounce_vect(38) or self.get_magnitude(new_vect) < self.get_magnitude(self.get_bot_bounce_vect(38))):
					
				# 	self.ball[0] += new_vect[0]				
				# 	self.ball[1] += new_vect[1]
				# 	self.has_wall = True
				# 	await asyncio.sleep(0.05)					
				# 	# self.has_wall = False
				# 	mag = self.get_magnitude(self.vect) 				
				# 	y = (self.ball[1] - self.pads_y[0]) / (self.pad_height / 2) 
				# 	y = y * mag
				# 	y = max(min(y, 0.9), -0.9)
				# 	x = (self.vect[0] ** 2) + (self.vect[1] ** 2) - (y ** 2)								
				# 	x = math.sqrt(abs(x))	

				# 	scl = 1
				# 	if abs(self.vect[0]) < self.max_speed and abs(self.vect[1]) < self.max_speed:
				# 		scl = self.acceleration
				# 	self.vect[0] = scl * x
				# 	self.vect[1] = scl * y 
				
				# 	self.flag = False
								
				# if  (self.ball[0] + self.vect[0] >= 84) and \
				# 	self.segments_intersect((self.ball[0], self.ball[1]), (self.ball[0] + self.vect[0], self.ball[1] + self.vect[1]), (84, self.pads_y[1] - (self.pad_height / 2)), (84, self.pads_y[1] + (self.pad_height / 2))):
				# 		# (self.pads_y[1] - (self.pad_height / 2) <= self.ball[1] + self.vect[1] <= self.pads_y[1] + (self.pad_height / 2)):			
					
				# 	new_vect = [0, 0]
				# 	new_vect[0] = 84 - self.ball[0]
				# 	new_vect[1] = self.scale_vector(new_vect[0], self.vect[1], self.vect[0])

				# 	# if (not self.get_top_bounce_vect(0) or self.get_magnitude(new_vect) < self.get_magnitude(self.get_top_bounce_vect(0))) and \
		 		# 	# 	(not self.get_bot_bounce_vect(38) or self.get_magnitude(new_vect) < self.get_magnitude(self.get_bot_bounce_vect(38))):

				# 	# await asyncio.sleep(0.5)	
				# 	self.ball[0] += new_vect[0]	
				# 	self.ball[1] += new_vect[1]
				# 	self.has_wall = True
				# 	await asyncio.sleep(0.05)
				# 	# self.has_wall = False				
				# 	mag = self.get_magnitude(self.vect) 					
				# 	y = (self.ball[1] - self.pads_y[1]) / (self.pad_height / 2) 
				# 	y = y * mag
				# 	y = max(min(y, 0.9), -0.9)
				# 	x = (self.vect[0] ** 2) + (self.vect[1] ** 2) - (y ** 2)
				# 	x = math.sqrt(abs(x))
				# 	scl = 1
				# 	if abs(self.vect[0]) < self.max_speed and abs(self.vect[1]) < self.max_speed:
				# 		scl = self.acceleration
				# 	self.vect[0] = -scl * x
				# 	self.vect[1] = scl * y 
				# 	# print(f"vect: {self.vect}", flush=True)
				
				# 	self.flag = False

				
						
				if (self.flag):	
					self.ball[0] += self.vect[0]				
					self.ball[1] += self.vect[1]
						
			else:
				if self.start_flag:
					if self.player1:
						self.winner = self.plyIds[0]
					elif self.player2:
						self.winner = self.plyIds[1]
				self.state = State.waiting
							
			await asyncio.sleep(0.05)	
		print(f"in match after WHILE id:{self.id}", flush=True)

	def segments_intersect(self, A, B, C, D, epsilon=1e-9):
		def orientation(p, q, r):
			# Déterminant orienté
			val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
			if abs(val) < epsilon:
				return 0  # colinéaire
			return 1 if val > 0 else 2  # 1: horaire, 2: anti-horaire

		def on_segment(p, q, r):
			# Vérifie si q est sur le segment [p, r]
			return (
				min(p[0], r[0]) - epsilon <= q[0] <= max(p[0], r[0]) + epsilon and
				min(p[1], r[1]) - epsilon <= q[1] <= max(p[1], r[1]) + epsilon
			)

		o1 = orientation(A, B, C)
		o2 = orientation(A, B, D)
		o3 = orientation(C, D, A)
		o4 = orientation(C, D, B)

		# Cas général
		if o1 != o2 and o3 != o4:
			return True

		# Cas particuliers (colinéaires)
		if o1 == 0 and on_segment(A, C, B): return True
		if o2 == 0 and on_segment(A, D, B): return True
		if o3 == 0 and on_segment(C, A, D): return True
		if o4 == 0 and on_segment(C, B, D): return True

		return False

	# def get_left_bounce_vect(self, left_y):
	# 	bounce_vect = None
	# 	if ((self.ball[0] + self.vect[0]) <= left_y) and \
	# 		(self.pads_y[0] - (self.pad_height / 2) <= self.ball[1] + self.vect[1] <= self.pads_y[0] + (self.pad_height / 2)):
		
	# 		bounce_vect = [0, 0]
	# 		bounce_vect[0] = left_y - self.ball[0]
	# 		bounce_vect[1] = self.scale_vector(bounce_vect[0], self.vect[1], self.vect[0])
	# 	return bounce_vect

	# def get_right_bounce_vect(self, right_y):
	# 	bounce_vect = None
	# 	if  (self.ball[0] + self.vect[0] >= right_y) and \
	# 		self.segments_intersect(self.vect[0], self.vect[1], self.pads_y[1] - (self.pad_height / 2), self.pads_y[1] + (self.pad_height / 2)):

	# 		# (self.pads_y[1] - (self.pad_height / 2) <= self.ball[1] + self.vect[1] <= self.pads_y[1] + (self.pad_height / 2)):			
				
	# 		bounce_vect = [0, 0]
	# 		bounce_vect[0] = right_y - self.ball[0]
	# 		bounce_vect[1] = self.scale_vector(bounce_vect[0], self.vect[1], self.vect[0])
	# 	return bounce_vect
		
	# def get_top_bounce_vect(self, top_y):
	# 	bounce_vect = None
	# 	if self.ball[1] + self.vect[1] <= top_y :
	# 		bounce_vect = [0, 0]
	# 		bounce_vect[1] = top_y - self.ball[1]
	# 		bounce_vect[0] = self.scale_vector(bounce_vect[1], self.vect[0], self.vect[1])
	# 	return bounce_vect

	# def get_bot_bounce_vect(self, bot_y):
	# 	bounce_vect = None
	# 	if self.ball[1] + self.vect[1] >= bot_y:	
	# 		bounce_vect = [0, 0]
	# 		bounce_vect[1] = bot_y - self.ball[1]
	# 		bounce_vect[0] = self.scale_vector(bounce_vect[1], self.vect[0], self.vect[1])
	# 	return bounce_vect

	def is_pad_intersecting(self, cmp, limit, pad_y_index):

		return cmp(self.ball[0] + self.vect[0], limit) and \
			self.segments_intersect(
				(self.ball[0], self.ball[1]),
				(self.ball[0] + self.vect[0], self.ball[1] + self.vect[1]),
				(limit, self.pads_y[pad_y_index] - (self.pad_height / 2)),
				(limit, self.pads_y[pad_y_index] + (self.pad_height / 2)))
		
	def are_pads_intersecting(self):

		return \
			self.is_pad_intersecting(op.ge, limit=84, pad_y_index=1) or \
			self.is_pad_intersecting(op.le, limit=16, pad_y_index=0)
		
	async def vert_bounce(self, cmp, limit):
		
		if self.are_pads_intersecting():
			return
		if cmp(self.ball[1] + self.vect[1], limit) :
			bounce_vect = [0, 0]
			bounce_vect[1] = limit - self.ball[1]
			bounce_vect[0] = self.scale_vector(
				bounce_vect[1], self.vect[0], self.vect[1])		
			self.ball[0] += bounce_vect[0]				
			self.ball[1] += bounce_vect[1]
			self.has_wall = True
			await asyncio.sleep(0.05)	
			self.vect[1] = -self.vect[1]		
			self.flag = False	

	# async def top_bounce(self, top_y):
		
	# 	if  (self.ball[0] + self.vect[0] >= 84) and \
	# 		self.segments_intersect((self.ball[0], self.ball[1]), (self.ball[0] + self.vect[0], self.ball[1] + self.vect[1]), (84, self.pads_y[1] - (self.pad_height / 2)), (84, self.pads_y[1] + (self.pad_height / 2))):
	# 		return 		
	# 	if ((self.ball[0] + self.vect[0]) <= 16) and \
	# 		self.segments_intersect((self.ball[0], self.ball[1]), (self.ball[0] + self.vect[0], self.ball[1] + self.vect[1]), (16, self.pads_y[0] - (self.pad_height / 2)), (16, self.pads_y[0] + (self.pad_height / 2))):
	# 		return 
	# 	if self.ball[1] + self.vect[1] <= top_y :
	# 		bounce_vect = [0, 0]
	# 		bounce_vect[1] = top_y - self.ball[1]
	# 		bounce_vect[0] = self.scale_vector(bounce_vect[1], self.vect[0], self.vect[1])

	# 		# if (not self.get_left_bounce_vect(16) or self.get_magnitude(bounce_vect) < self.get_magnitude(self.get_left_bounce_vect(16))) and \
	# 		# 	(not self.get_right_bounce_vect(84) or self.get_magnitude(bounce_vect) < self.get_magnitude(self.get_right_bounce_vect(84))):
	# 		self.ball[0] += bounce_vect[0]				
	# 		self.ball[1] += bounce_vect[1]
	# 		self.has_wall = True
	# 		await asyncio.sleep(0.05)
	# 		# self.has_wall = False
	# 		self.vect[1] = -self.vect[1]		
	# 		self.flag = False

	# async def bot_bounce(self, bot_y):

	# 	if  (self.ball[0] + self.vect[0] >= 84) and \
	# 		self.segments_intersect((self.ball[0], self.ball[1]), (self.ball[0] + self.vect[0], self.ball[1] + self.vect[1]), (84, self.pads_y[1] - (self.pad_height / 2)), (84, self.pads_y[1] + (self.pad_height / 2))):
	# 		return 		
	# 	if ((self.ball[0] + self.vect[0]) <= 16) and \
	# 		self.segments_intersect((self.ball[0], self.ball[1]), (self.ball[0] + self.vect[0], self.ball[1] + self.vect[1]), (16, self.pads_y[0] - (self.pad_height / 2)), (16, self.pads_y[0] + (self.pad_height / 2))):
	# 		return 
	# 	if self.ball[1] + self.vect[1] >= bot_y:					
	# 		bounce_vect = [0, 0]
	# 		bounce_vect[1] = bot_y - self.ball[1]
	# 		bounce_vect[0] = self.scale_vector(bounce_vect[1], self.vect[0], self.vect[1])

	# 		# if (not self.get_left_bounce_vect(16) or self.get_magnitude(bounce_vect) < self.get_magnitude(self.get_left_bounce_vect(16))) and \
	# 		# 	(not self.get_right_bounce_vect(84) or self.get_magnitude(bounce_vect) < self.get_magnitude(self.get_right_bounce_vect(84))):
			
	# 		self.ball[0] += bounce_vect[0]				
	# 		self.ball[1] += bounce_vect[1]
	# 		self.has_wall = True
	# 		await asyncio.sleep(0.05)
	# 		# self.has_wall = False
	# 		self.vect[1] = -self.vect[1]
	# 		self.flag = False

	def get_magnitude(self, vect):
		return math.sqrt(vect[0] ** 2 + vect[1] ** 2)
		
	# def scale_vector(self, nx,  x, y, nx):
	# 	return nx * y / x

	def scale_vector(self, m1, m2, div):
		return m1 * m2 / div

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
				await self.stop(self.plyIds[0])
				return
			delay += 1
			await asyncio.sleep(1.00)

	async def sendState(self):		
		while self.state != State.end:	
			# print(f"{self.ball}", flush=True)
			self.myplayers = [p for p in consumer.players
				if self.id == p["matchId"]]
			for p in self.myplayers:
				state = self.state
				if state != State.end:
					try:												
						await p["socket"].send(text_data=json.dumps({
							"state": state.name,
							"yp1": self.pads_y[0],
							"yp2": self.pads_y[1],
							"ball": self.ball,
							"score": self.score,
							"hasWall": self.has_wall
						}))                  
					except Exception as e:
						pass				
			await asyncio.sleep(0.05)

	async def sendFinalState(self):	
		print(f"SEND FINAL STATE", flush=True)			
		self.myplayers = [p for p in consumer.players
			if self.id == p["matchId"]]
		for p in self.myplayers:
			print(f"myplayers {p}", flush=True)
			try:					
				await p["socket"].send(text_data=json.dumps({
				"state": self.state.name,
				"winnerId": self.winner,
				"score": self.score
				}))
			except Exception as e:
				pass		
		print(f"BEFORE SEND MATCH RESULT", flush=True)


		# response = requests.post(
		# 	"http://tournament:8001/tournament/match-result/", json={
		# 	"matchId": self.id,
		# 	"winnerId": self.winner,
		# 	"looserId": self.idP1 if self.winner == self.idP2 else self.idP2,
		# 	"p1Id": self.idP1,
		# 	"p2Id": self.idP2,
		# 	"score": self.score
		# })

		# if response.status_code not in [200, 201]:
		# 	print(f"Error HTTP {response.status_code}: {response.text}")

		async with aiohttp.ClientSession() as session:
			async with session.post(
				"http://tournament:8001/tournament/match-result/", json={
				"matchId": self.id,
				"winnerId": self.winner,
				"looserId": self.plyIds[0] if self.winner == self.plyIds[1]
					else self.plyIds[1],
				"p1Id": self.plyIds[0],
				"p2Id": self.plyIds[1],
				"score": self.score
			}) as response:
				print(f"RESPONSE HTTP {response.status}", flush=True)
				if response.status != 200 and response.status != 201:
					err = await response.text()
					print(f"Error HTTP {response.status}: {err}", flush=True)
		print(f"AFTER SEND MATCH RESULT", flush=True)
		from match_app.views import del_pong
		del_pong(self.id)			
