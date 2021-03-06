# -*- coding: utf-8 -*-
import os
from abc import ABCMeta, abstractmethod
import Pyro4
import serpent


class AbstractStorage(object):
    """Implementa a interface Storage"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, file, filename):
        """Colocar definição aqui."""
        return

    @abstractmethod
    def delete(self):
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
        self.pk = self.proxy.n_servers
        self.db = "storage-secondary-{0}".format(self.pk)
        self.name = "storage.server.secundary.id-{0}".format(self.pk)
        self.proxy.register(self.name)

        try:
            os.mkdir(self.db)
        except:
            pass

        self._sync()

    @Pyro4.oneway
    def save(self, file, filename):
        with open(os.path.join(self.db, filename), "wb") as f:
            f.write(serpent.tobytes(file))

    def delete(self, filename):
        response = {'code': '404', 'content': 'Not found.'}

        try:
            os.remove(os.path.join(self.db, filename))
            response['code'] = '200'
            response['content'] = 'Arquivo deletado.'
        except:
            pass

        return response

    def retrieve(self, filename):
        response = {'code': '404', 'content': 'Not found.'}
        try:
            with open(os.path.join(self.db, filename), "rb") as f:
                response['code'] = '200'
                response['content'] = f.read()
        except:
            self._sync()

        return response

    def list(self):
        response = {'code': '404', 'content': 'Not found.'}

        response['code'] = '200'
        response['content'] = os.listdir(self.db)

        return response

    def _sync(self):
        with Pyro4.Proxy("PYRONAME:storage.server.primary") as primary:

            primary_files = set(primary.list()['content'])

            my_files = set(self.list()['content'])

            sync_files = primary_files - my_files

            for filename in sync_files:
                response = primary.retrieve(filename)
                self.save(serpent.tobytes(response['content']), filename)

            delete_files = my_files - primary_files

            for filename in delete_files:
                os.remove(os.path.join(self.db, filename))

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

        with open(os.path.join(self.db, filename), "wb") as f:
            f.write(serpent.tobytes(file))

        for server_name in self.proxy.servers:
            if server_name != self.name:
                with Pyro4.Proxy("PYRONAME:" + server_name) as storage:
                    try:
                        storage._pyroBind()
                        storage.save(serpent.tobytes(file), filename)
                    except:
                        print("Err: Objeto não encontrado...")

    def delete(self, filename):
        response = {'code': '404', 'content': 'Not found.'}

        try:
            os.remove(os.path.join(self.db, filename))
            response['code'] = '200'
            response['content'] = 'Arquivo deletado.'
        except:
            pass

        for server_name in self.proxy.servers:
            if server_name != self.name:
                with Pyro4.Proxy("PYRONAME:" + server_name) as storage:
                    try:
                        storage._pyroBind()
                        storage.delete(filename)
                    except:
                        print("Err: Objeto não encontrado...")

        return response

    def retrieve(self, filename):
        response = {'code': '404', 'content': 'Not found.'}

        try:
            with open(os.path.join(self.db, filename), "rb") as f:
                response['code'] = '200'
                response['content'] = f.read()
        except:
            pass

        return response

    def list(self):
        response = {'code': '404', 'content': 'Not found.'}

        response['code'] = '200'
        response['content'] = os.listdir(self.db)

        return response


@Pyro4.expose
class StorageProxy(AbstractStorage):

    def __init__(self):
        self._servers = list()
        self._n_servers = 0

    @Pyro4.oneway
    def save(self, file, filename):
        """Colocar definição aqui."""
        with Pyro4.Proxy("PYRONAME:storage.server.primary") as primary:
            primary.save(file, filename)

    def delete(self, filename):
        """Colocar definição aqui."""
        response = {'code': '404', 'content': 'Not found.'}

        with Pyro4.Proxy("PYRONAME:storage.server.primary") as primary:
            response = primary.delete(filename)

        return response

    def retrieve(self, filename):
        """Colocar definição aqui."""
        ctrl = True
        while ctrl:
            server_name = self._servers.pop()
            self._servers.insert(0, server_name)
            storage = Pyro4.Proxy("PYRONAME:" + server_name)
            try:
                storage._pyroBind()
                print("Lendo do server: " + server_name)
                ctrl = False
            except:
                pass

        if filename in self.list()['content']:
            response = storage.retrieve(filename)

            if response['code'] == '404' and server_name != 'storage.server.primary':
                with Pyro4.Proxy("PYRONAME:storage.server.primary") as primary:
                    response = primary.retrieve(filename)
                    print('Server {0} falhou. Recebendo resposta do primário...'.format(
                        server_name))

            return response

        else:
            response = {'code': '404', 'content': 'Not found.'}
            return response

    def list(self):
        """Colocar definição aqui."""
        with Pyro4.Proxy("PYRONAME:storage.server.primary") as primary:
            response = primary.list()

        return response

    def register(self, server_name):
        self._servers.append(server_name)
        self._n_servers += 1

    @property
    def servers(self):
        return self._servers

    @property
    def n_servers(self):
        return self._n_servers
