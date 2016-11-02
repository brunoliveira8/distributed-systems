from StorageServer import *
import Pyro4


def main():

    proxy = StorageProxy()
    primary = StoragePrimary(proxy)

    with Pyro4.Daemon() as daemon:

        with Pyro4.locateNS() as ns:
            uri = daemon.register(proxy)
            ns.register("storage.proxy", uri)

            uri = daemon.register(primary)
            ns.register("storage.server.primary", uri)

        print("\n Running...")
        daemon.requestLoop()


if __name__ == '__main__':
    main()
