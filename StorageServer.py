#-*- coding: utf-8 -*-
import os
import Pyro4

@Pyro4.expose
class StorageServer:
	
	n_count = 0

	def __init__(self):
		self.pk = StorageServer.n_count+1
		self.db = "storage-{0}".format(self.pk)
		try:
			os.mkdir(self.db)
		except:
			pass

		StorageServer.n_count+=1

	def save(self, file, filename):
		with open(os.path.join(self.db, filename), "w") as f:
			f.write(file)


	def retrieve(self, filename):
		with open(os.path.join(self.db, filename), "r") as f:
			data = f.read()
			return data


	def list(self):
		data = os.listdir(self.db)
		return data


def main():
	
	n_servers = 2
	servers = list()

	for _ in range(n_servers):
		servers.append(StorageServer())
	

	with Pyro4.Daemon() as daemon:
		with Pyro4.locateNS() as ns:
			for server in servers:
				uri = daemon.register(server)
				ns.register("storage.server-{0}".format(server.pk), uri)

		print("{} servers registered.".format(n_servers))
		print("\n Running...")

		daemon.requestLoop()


if __name__ == '__main__':
	main()