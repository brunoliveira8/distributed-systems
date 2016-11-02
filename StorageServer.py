# -*- coding: utf-8 -*-
import os
from abc import ABCMeta, abstractmethod
import Pyro4


class AbstractStorage(object):
    """Implementa a interface Storage"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, file, filename):
        """Colocar definição aqui."""
        return

    @abstractmethod
    def retrieve(self, filename):
        """Colocar definição aqui."""
        return

    @abstractmethod
    def list(self):
        """Colocar definição aqui."""
        return


@Pyro4.expose
class StorageSecundary(AbstractStorage):

    def __init__(self, proxy):
        self.proxy = proxy
        self.pk = self.proxy.get_n_servers()
        self.db = "storage-secondary-{0}".format(self.pk)
        self.name = "storage.server.secundary.id-{0}".format(self.pk)
        self.proxy.register(self.name)

        try:
            os.mkdir(self.db)
        except:
            pass

    @Pyro4.oneway
    def save(self, file, filename):
        with open(os.path.join(self.db, filename), "w") as f:
            f.write(file)

    def retrieve(self, filename):
        with open(os.path.join(self.db, filename), "r") as f:
            response = f.read()
            return response

    def list(self):
        response = os.listdir(self.db)
        return response


@Pyro4.expose
class StoragePrimary(AbstractStorage):

    def __init__(self, proxy):

        self.db = "storage-primary"
        self.name = "storage.server.primary"
        self.proxy = proxy

        self.proxy.register(self.name)

        try:
            os.mkdir(self.db)
        except:
            pass

    @Pyro4.oneway
    def save(self, file, filename):
        with open(os.path.join(self.db, filename), "w") as f:
            f.write(file)

        for server_name in self.proxy.servers:
            if server_name != self.name:
                with Pyro4.Proxy("PYRONAME:" + server_name) as storage:
                    storage.save(file, filename)

    def retrieve(self, filename):
        with open(os.path.join(self.db, filename), "r") as f:
            response = f.read()
            return response

    def list(self):
        response = os.listdir(self.db)
        return response


@Pyro4.expose
class StorageProxy(AbstractStorage):

    def __init__(self):
        self.servers = list()
        self.n_servers = 0

    @Pyro4.oneway
    def save(self, file, filename):
        """Colocar definição aqui."""
        with Pyro4.Proxy("PYRONAME:storage.server.primary") as primary:
            primary.save(file, filename)

    def retrieve(self, filename):
        """Colocar definição aqui."""
        server_name = self.servers.pop()
        self.servers.insert(0, server_name)
        storage = Pyro4.Proxy("PYRONAME:" + server_name)
        response = storage.retrieve(filename)
        print("Lendo do server: " + server_name)

        return response

    def list(self):
        """Colocar definição aqui."""
        server_name = self.servers.pop()
        self.servers.insert(0, server_name)
        storage = Pyro4.Proxy("PYRONAME:" + server_name)
        response = storage.list()
        print("Lendo do server: " + server_name)

        return response

    def register(self, server_name):
        self.servers.append(server_name)
        self.n_servers += 1

    def get_n_servers(self):
        return self.n_servers
