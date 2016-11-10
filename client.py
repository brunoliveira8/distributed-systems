# -*- coding: utf-8 -*-
import os
import Pyro4


def main():

    storage = Pyro4.Proxy("PYRONAME:storage.proxy")
    #storage.save("hi, friend", "hello1.txt")
    print(storage.retrieve("hello1.txt"))
    print(storage.list())


if __name__ == '__main__':
    main()
