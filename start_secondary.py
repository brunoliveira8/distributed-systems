from StorageServer import *
import Pyro4


def main():

    n_servers = 1
    servers = list()

    with Pyro4.Proxy("PYRONAME:storage.proxy") as proxy:

        for _ in range(n_servers):
            servers.append(StorageSecundary(proxy))

        with Pyro4.Daemon() as daemon:

            with Pyro4.locateNS() as ns:

                for server in servers:
                    uri = daemon.register(server)
                    ns.register(server.name, uri)

            print("{} servers registered.".format(n_servers))
            print("\n Running...")

            daemon.requestLoop()


if __name__ == '__main__':
    main()
