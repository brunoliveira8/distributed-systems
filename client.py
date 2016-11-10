# -*- coding: utf-8 -*-
import os
import Pyro4


def main():

    storage = Pyro4.Proxy("PYRONAME:storage.proxy")
    # storage.save("hi, friend", "hello.txt")
    print(storage.retrieve("hello.txt"))
    print(storage.list())
    print(storage.delete("hello.txt"))


if __name__ == '__main__':
    main()
