import threading
import time
import StorageServer
import Pyro4

daemons = list()
daemons_secondary = dict()
secondary_servers = dict()


class NSThread(threading.Thread):
    def run(self):
        _, daemon, _ = Pyro4.naming.startNS()
        daemons.append(daemon)
        daemon.requestLoop()


class ProxyThread(threading.Thread):
    def run(self):
        proxy = StorageServer.StorageProxy()

        with Pyro4.Daemon() as daemon:
            daemons.append(daemon)

            with Pyro4.locateNS() as ns:
                uri = daemon.register(proxy)
                ns.register("storage.proxy", uri)

            daemon.requestLoop()


class PrimaryThread(threading.Thread):
    def run(self):
        with Pyro4.Proxy("PYRONAME:storage.proxy") as proxy:
            primary = StorageServer.StoragePrimary(proxy)

            with Pyro4.Daemon() as daemon:
                daemons.append(daemon)

                with Pyro4.locateNS() as ns:

                    uri = daemon.register(primary)
                    ns.register("storage.server.primary", uri)

                daemon.requestLoop()


class SecondaryThread(threading.Thread):
    def run(self):
        with Pyro4.Proxy("PYRONAME:storage.proxy") as proxy:
            server = StorageServer.StorageSecundary(proxy)
            secondary_servers[server.name] = server

            with Pyro4.Daemon() as daemon:

                with Pyro4.locateNS() as ns:

                    uri = daemon.register(server)
                    ns.register(server.name, uri)

                    daemons_secondary[server.name] = daemon

                daemon.requestLoop()


def desregistrar_servidor(server_id):
    server_name = "storage.server.secundary.id-{0}".format(server_id)
    daemon = daemons_secondary[server_name]
    server = secondary_servers[server_name]
    daemon.unregister(server)


def registrar_servidor(server_id):
    server_name = "storage.server.secundary.id-{0}".format(server_id)
    daemon = daemons_secondary[server_name]
    server = secondary_servers[server_name]
    uri = daemon.register(server)
    with Pyro4.locateNS() as ns:
        ns.register(server_name, uri)


def main():
    running = True
    while running:
        commands = """
        Bem vindo!

        Digite a opção desejada:

        1 - Inicializar (Cria Proxy e Primário)
        2 - Criar Secundário
        3 - Desregistrar Secundário
        4 - Registrar Secundário
        5 - Sair
        """
        print(commands)

        opt = int(input("\tInput: "))

        if opt == 1:
            thread = NSThread()
            thread.start()
            print("\tName Server ativo...")

            time.sleep(0.5)

            thread = ProxyThread()
            thread.start()
            print("\tProxy está ativo com uri 'storage.proxy'...")

            time.sleep(0.5)

            thread = PrimaryThread()
            thread.start()
            print("\tCópia Primária está ativa com uri 'storage.server.primary'...")

            time.sleep(0.5)

        elif opt == 2:
            thread = SecondaryThread()
            thread.start()
            print("\tUma cópia secundária foi criada...")

        elif opt == 3:
            server_id = input("\tDigite o id do servidor: ")
            desregistrar_servidor(server_id)

        elif opt == 4:
            server_id = input("\tDigite o id do servidor: ")
            registrar_servidor(server_id)

        elif opt == 5:
            for daemon in daemons:
                daemon.shutdown()

            for daemon in daemons_secondary.values():
                daemon.shutdown()

            running = False
        else:
            print("\tDigite uma opção válida")


if __name__ == '__main__':
    main()
