#-*- coding: utf-8 -*-
import os
import Pyro4

def main():

	storage = Pyro4.Proxy("PYRONAME:storage.server-1")
	print(storage.retrieve("name.txt"))

if __name__ == '__main__':
	main()