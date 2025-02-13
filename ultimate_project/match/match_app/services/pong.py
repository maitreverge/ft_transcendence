import threading
import time

import match_app.services.consumer as consumer

import asyncio

# class Pong:

# 	id = 0
# 	def __init__(self):
# 		Pong.id += 1
# 		self.id = Pong.id
# 		# self.players = players
# 		threading.Thread(target=self.launch, daemon=True).start()

# 	def launch(self):
# 		while (True):			
# 			print(f"game state {self.id}" , flush=True)
# 			self.sendState()
# 			time.sleep(1)

# 	def sendState(self):
# 		print(consumer.players)
# 		self.myplayers = [p for p in consumer.players if self.id == p["matchId"]]
# 		print(self.myplayers)
# 		for p in self.myplayers:	
# 			print(f"send state {self.id}", flush=True)
# 			p["socket"].send(text_data="youhou")

class Pong:

	id = 0
	def __init__(self):
		Pong.id += 1
		self.id = Pong.id
		# self.players = players
		print("launch init" , flush=True)
		threading.Thread(target=self.launchTask, daemon=True).start()

	def launchTask(self):
		print("launch task" , flush=True)
		self.myEventLoop = asyncio.new_event_loop()
		asyncio.set_event_loop(self.myEventLoop)
		self.myEventLoop.create_task(self.launch())
		self.myEventLoop.run_forever()
		# myEventLoop.run_until_complete(asyncio.Future())
		# myEventLoop.run_until_complete(self.launch())

	async def launch(self):
		self.myEventLoop.create_task(self.sendState())
		while (True):			
			print(f"game state {self.id}" , flush=True)
			# await self.sendState()
			await asyncio.sleep(1)

	# async def sendState(self):
	# 	while (True):
	# 		time.sleep(5)
	# 		print("SEND" , flush=True)
	async def sendState(self):
		while (True):
			print(consumer.players)
			self.myplayers = [p for p in consumer.players if self.id == p["matchId"]]
			print(self.myplayers)
			for p in self.myplayers:	
				print(f"send state {self.id}", flush=True)
				await p["socket"].send(text_data=f"youhou {self.id} et {p['matchId']}")
			# time.sleep(1)
			await asyncio.sleep(1)



# class Pong:
#     id = 0
#     def __init__(self):
#         Pong.id += 1
#         self.id = Pong.id
#         # On lance la coroutine dans l'event loop, qui doit être déjà active
#         asyncio.create_task(self.launch())

#     async def launch(self):
#         while True:
#             print(f"game state {self.id}", flush=True)
#             await self.sendState()
#             await asyncio.sleep(1)

#     async def sendState(self):
#         print(consumer.players)
#         self.myplayers = [p for p in consumer.players if self.id == int(p["matchId"])]
#         print(self.myplayers)
#         # Lancer les envois sans attendre chaque envoi (fire-and-forget)
#         for p in self.myplayers:
#             print(f"send state {self.id}", flush=True)
#             # Ici on peut créer une tâche pour envoyer le message sans attendre sa fin
#             asyncio.create_task(p["socket"].send(text_data="youhou"))
# import types
# class Pong:
# 	id = 0
# 	def __init__(self):
# 		Pong.id += 1
# 		self.id = Pong.id
# 		# On lance la coroutine dans l'event loop, qui doit être déjà active
# 		asyncio.create_task(self.f())

# 	def mon_generateur(self):
# 		yield "première valeur"   # La fonction retourne "première valeur" et se suspend ici
# 		yield "deuxième valeur"   # Au prochain appel, elle reprend ici et retourne "deuxième valeur"
# 		yield "troisième valeur"  # Et ainsi de suite

   	
# 	async def f(self):
# 		# print("début", flush=True)
# 		# print(next(self.mon_generateur()))
# 		# print("entre1", flush=True)
# 		# print(next(self.mon_generateur()))
# 		# print("entre2", flush=True)
# 		# print(next(self.mon_generateur()))
# 		# print("entre3", flush=True)
# 		# print(next(self.mon_generateur()))
# 		# print("entre4", flush=True)
# 		# On lance la tâche foo en parallèle
# 		asyncio.create_task(self.foo())
# 		# await asyncio.sleep(0)
		
# 		await self.launch()  # On attend la fin de launch()
# 		print("fin", flush=True)
		
# 	@types.coroutine
# 	def launch(self):
# 		yield
# 		print("launch", flush=True)	
# 		# await self.truc()    # On attend que truc() se termine
# 		print("launch2", flush=True)
# 		print("launch3", flush=True)

# 	async def truc(self):
# 		print("truc", flush=True)

# 	async def foo(self):
# 		print("foo", flush=True)
