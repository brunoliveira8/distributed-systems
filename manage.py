import threading
import time
import StorageServer
import Pyro4

daemons = []


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


def main():
    running = True
    while running:
        commands = """
        Bem vindo!

        Digite a opção desejada:

        1 - Inicializar (Cria Proxy e Primário)
        4 - Criar Secundário
        4 - Deletar Secundário
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
            pass
        elif opt == 3:
            pass
        elif opt == 4:
            pass
        elif opt == 5:
            for daemon in daemons:
                daemon.shutdown()
            running = False
        else:
            print("\tDigite uma opção válida")


if __name__ == '__main__':
    main()
